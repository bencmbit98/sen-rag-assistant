import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    _TEXT_SPLITTER_AVAILABLE = True
except Exception:
    _TEXT_SPLITTER_AVAILABLE = False
import tempfile
import openai

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SEN RAG Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 SEN Guidelines RAG Assistant")
st.markdown("Ask questions about Special Educational Needs guidelines and resources")

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Load API key from environment (Streamlit secrets)
    api_key_env = os.getenv("OPENAI_API_KEY", "")
    
    if api_key_env:
        # Secret is already set - use it silently
        api_key = api_key_env
        st.success("✅ OpenAI API key loaded from secrets")
    else:
        # No secret - show input field
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key (or set as Streamlit secret)"
        )
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    
    # Initialize OpenAI client
    if api_key:
        try:
            st.session_state.openai_client = openai.OpenAI(api_key=api_key)
        except Exception:
            openai.api_key = api_key
    
    # Load documents button
    if st.button("📖 Load Documents", use_container_width=True):
        if not api_key:
            st.error("❌ Please provide an OpenAI API key first")
        else:
            with st.spinner("Processing documents..."):
                try:
                    # Load all PDFs from docs folder
                    docs_folder = "docs"
                    documents = []
                    
                    for filename in os.listdir(docs_folder):
                        if filename.endswith(".pdf"):
                            filepath = os.path.join(docs_folder, filename)
                            loader = PyPDFLoader(filepath)
                            documents.extend(loader.load())
                            st.success(f"✓ Loaded {filename}")
                    
                    if not documents:
                        st.error("❌ No PDF files found in docs folder")
                    else:
                        # Split documents into chunks
                        st.info(f"Processing {len(documents)} pages...")

                        def _chunk_text(text, chunk_size=1000, chunk_overlap=200):
                            if not text:
                                return []
                            chunks = []
                            start = 0
                            text_len = len(text)
                            while start < text_len:
                                end = start + chunk_size
                                chunk = text[start:end]
                                chunks.append(chunk)
                                if end >= text_len:
                                    break
                                start = end - chunk_overlap
                            return chunks

                        chunks = []
                        metadatas = []

                        if _TEXT_SPLITTER_AVAILABLE:
                            text_splitter = RecursiveCharacterTextSplitter(
                                chunk_size=1000,
                                chunk_overlap=200,
                                separators=["\n\n", "\n", " ", ""]
                            )
                            split_docs = text_splitter.split_documents(documents)
                            for d in split_docs:
                                chunks.append(d.page_content)
                                metadatas.append(d.metadata if hasattr(d, 'metadata') else {})
                        else:
                            for d in documents:
                                text = getattr(d, "page_content", str(d))
                                src_meta = getattr(d, "metadata", {})
                                subchunks = _chunk_text(text, chunk_size=1000, chunk_overlap=200)
                                for sc in subchunks:
                                    chunks.append(sc)
                                    metadatas.append(src_meta)

                        st.success(f"✓ Split into {len(chunks)} chunks")
                        
                        # Create embeddings and vector store
                        st.info("Creating vector store...")
                        embeddings = OpenAIEmbeddings()
                        # Use from_texts with metadata if available
                        try:
                            vector_store = FAISS.from_texts(chunks, embeddings, metadatas=metadatas)
                        except Exception:
                            # Fallback: try from_documents if installed and chunks are Document objects
                            vector_store = FAISS.from_documents(chunks, embeddings)
                        
                        # Save vector store
                        vector_store.save_local("faiss_index")
                        st.session_state.vector_store = vector_store
                        st.session_state.documents_loaded = True
                        
                        st.success("✅ Documents loaded and indexed successfully!")
                except Exception as e:
                    st.error(f"❌ Error loading documents: {str(e)}")
    
    # Load existing vector store
    if st.button("📂 Load Existing Index", use_container_width=True):
        if not api_key:
            st.error("❌ Please provide an OpenAI API key first")
        else:
            try:
                embeddings = OpenAIEmbeddings()
                vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
                st.session_state.vector_store = vector_store
                st.session_state.documents_loaded = True
                st.success("✅ Loaded existing vector store!")
            except Exception as e:
                st.error(f"❌ Error loading vector store: {str(e)}")
    
    st.divider()
    st.markdown("**Status:**")
    if st.session_state.documents_loaded:
        st.success("✅ Documents loaded")
    else:
        st.warning("⚠️ No documents loaded")

# Main content area
if not st.session_state.documents_loaded:
    st.info(
        """
        👈 **Get Started:**
        1. Enter your OpenAI API key in the sidebar
        2. Click "Load Documents" to process the PDFs
        3. Ask questions about the SEN guidelines!
        
        **What this app does:**
        - Loads and processes PDF documents from the `docs` folder
        - Creates a searchable vector index using FAISS
        - Answers your questions using GPT-4 with context from the documents
        """
    )
else:
    # QA Section
    st.header("💬 Ask a Question")
    
    # Prepare LLM flag (we call OpenAI directly)
    if st.session_state.qa_chain is None and st.session_state.vector_store is not None:
        st.session_state.qa_chain = True
    
    # Question input
    question = st.text_area(
        "Enter your question:",
        placeholder="e.g., What are the guidelines for access arrangements for students with SEN?",
        height=100
    )
    
    if st.button("🔍 Get Answer", use_container_width=True):
        if not question:
            st.warning("⚠️ Please enter a question")
        else:
                with st.spinner("Searching and generating answer..."):
                    try:
                        # Retrieve top-k relevant chunks from vector store
                        k = 4
                        try:
                            docs = st.session_state.vector_store.similarity_search(question, k=k)
                        except Exception:
                            # fallback to retriever interface
                            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": k})
                            docs = retriever.get_relevant_documents(question)

                        passages = []
                        sources = []
                        for d in docs:
                            text = getattr(d, "page_content", None) or getattr(d, "text", None) or str(d)
                            passages.append(text)
                            src = getattr(d, "metadata", {}).get("source") if getattr(d, "metadata", None) else None
                            sources.append(src)

                        context = "\n\n---\n\n".join(passages)

                        system_prompt = (
                            "You are a helpful assistant. Use the provided context to answer the question. "
                            "If the answer is not contained in the context, say you don't know instead of hallucinating."
                        )

                        user_prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer concisely and cite sources when possible." 

                        # Call OpenAI ChatCompletion
                        model_name = os.getenv("OPENAI_MODEL", "gpt-4")
                        try:
                            client = st.session_state.get("openai_client") or openai.OpenAI()
                            resp = client.chat.completions.create(
                                model=model_name,
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": user_prompt},
                                ],
                                temperature=0.2,
                                max_tokens=800,
                            )
                            # Extract content from the new v1 API response
                            answer = resp.choices[0].message.content.strip()
                        except Exception as e:
                            st.error(f"❌ OpenAI API error: {str(e)}")
                            answer = None

                        if answer:
                            st.success("Answer found!")
                            st.markdown("### 📝 Answer:")
                            st.markdown(answer)
                            if any(s for s in sources):
                                st.markdown("### 📚 Sources:")
                                for s in set([s for s in sources if s]):
                                    st.markdown(f"- {s}")
                        else:
                            st.error("❌ Failed to generate an answer.")

                    except Exception as e:
                        st.error(f"❌ Error during retrieval/generation: {str(e)}")
    
    # Example questions
    with st.expander("📋 Example Questions"):
        examples = [
            "What are the guidelines for access arrangements?",
            "How should lecturers support HBL students?",
            "What is the student crisis support procedure?",
            "What languages are considered inclusive and disability-friendly?",
            "What are the misconduct management procedures for students with SEN?"
        ]
        for example in examples:
            if st.button(f"❓ {example}", key=example):
                st.session_state.question = example
