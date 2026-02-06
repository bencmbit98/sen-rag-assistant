# SEN Guidelines RAG Assistant

A Retrieval Augmented Generation (RAG) application built with Streamlit and LangChain that answers questions about Special Educational Needs guidelines and resources.

## Features

- 📚 **Document Processing**: Automatically loads and processes all PDF documents from the `docs` folder
- 🔍 **Semantic Search**: Uses FAISS vector database for fast, intelligent document retrieval
- 🤖 **AI-Powered Answers**: GPT-4 powered responses with context from your documents
- 💬 **Interactive UI**: User-friendly Streamlit interface for asking questions
- 📂 **Vector Store Caching**: Save and reuse your indexed documents for faster startup

## Project Structure

```
sen/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── README.md             # This file
├── docs/                 # PDF documents (10 SEN guidance files)
└── faiss_index/          # Vector store (auto-generated after first run)
```

## Requirements

- Python 3.8 or higher
- OpenAI API key with access to GPT-4
- Internet connection for API calls

## Setup Instructions

### 1. Clone the Repository

```bash
cd "c:\Users\benedict\OneDrive - Temasek Polytechnic\Ben Academic\Projects\Project FutureX\sen"
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
# Windows PowerShell
cp .env.example .env

# Windows CMD
copy .env.example .env
```

Then edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your_actual_api_key_here
```

**How to get an OpenAI API Key:**
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in your `.env` file

### 5. Run the Application Locally

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

1. **First Time Setup:**
   - Enter your OpenAI API key in the sidebar
   - Click "Load Documents" to process all PDFs from the `docs` folder
   - Wait for the vector store to be created (this may take a few minutes)

2. **Asking Questions:**
   - Type your question in the text area
   - Click "Get Answer" to retrieve and generate a response
   - The app will search the documents and provide an AI-generated answer

3. **Subsequent Runs:**
   - Click "Load Existing Index" to use the saved vector store
   - Much faster than processing documents again

## Deployment on Streamlit Cloud

### Prerequisites
- GitHub account
- Push your code to a GitHub repository

### Deployment Steps

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: SEN RAG Assistant"
   git remote add origin https://github.com/your-username/sen-rag-assistant.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch, and `app.py` as the main file
   - Click "Deploy"

3. **Add Secrets (for API Key):**
   - In the deployed app, click the "..." menu → Settings
   - Go to "Secrets"
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY = "sk-your_actual_api_key_here"
     ```

4. **Reboot the App:**
   - Click "Reboot" for the secrets to take effect

## Documents Included

The `docs` folder contains 10 PDF files:

1. Global-Studies-Overseas-Trip---SEN-guidelines-WEF-Jun-2024.pdf
2. Guidelines-for-Access-Arrangements-for-Students-with-Special-Educational-Needs--Effective-AY2022-April-Semester-.pdf
3. Guide_Management-of-Misconduct-and-Disciplinary-Cases-involving-Students-with-SEN_Final.pdf
4. HBL-Strategies-for-Lecturers.pdf
5. Inclusive-and-Disability-friendly-Language-2024.pdf
6. PC_Playbook_Dec25.pdf
7. SEN-Staff-Guide_Dec-2025.pdf
8. SEN-Support-Student-Handbook_Dec-2025.pdf
9. Student-Crisis-Support-Guide_as-of-10-June-2022.pdf
10. Student-Internship-Programme-Liaison-Officer-Navigator-Mar-24.pdf

## Architecture

```
User Question
    ↓
Streamlit UI Input
    ↓
OpenAI Embeddings (Convert question to vector)
    ↓
FAISS Vector Search (Find relevant document chunks)
    ↓
Retrieved Context + Question
    ↓
GPT-4 (Generate answer with context)
    ↓
Display Answer in Streamlit
```

## Customization

### Adjust Chunk Size
Edit `app.py` and modify the `chunk_size` parameter:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Increase for longer contexts
    chunk_overlap=200,
)
```

### Change Model
Edit the LLM initialization:
```python
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",  # Use gpt-3.5-turbo for cost savings
    temperature=0.7
)
```

### Adjust Retrieval Parameters
Edit the retriever kwargs:
```python
retriever=st.session_state.vector_store.as_retriever(
    search_kwargs={"k": 4}  # Return top 4 most relevant chunks
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Ensure `.env` file exists with valid `OPENAI_API_KEY` |
| "No module named 'langchain'" | Run `pip install -r requirements.txt` again |
| "FAISS index not found" | Click "Load Documents" to create a new index |
| "Rate limit exceeded" | Wait a few minutes before making another request |
| PDF not loading | Ensure PDF files are in `docs` folder and readable |

## Performance Notes

- **First load**: 2-5 minutes depending on PDF size and internet speed
- **Subsequent loads**: < 1 second (using cached vector store)
- **Question answering**: 5-15 seconds depending on API response time

## Costs

Using this application incurs costs from OpenAI:
- **Embeddings**: ~$0.01 per 1M tokens (one-time during document loading)
- **GPT-4**: ~$0.03 per 1K input tokens + $0.06 per 1K output tokens

Example: Loading documents + answering 10 questions ≈ $0.50-$1.00

## Future Enhancements

- [ ] Support for other document types (DOCX, TXT, HTML)
- [ ] Multi-user authentication
- [ ] Chat history and conversation context
- [ ] Document upload UI
- [ ] Multiple vector store management
- [ ] Cost tracking
- [ ] Integration with other LLMs (Claude, Gemini, Open-source models)

## License

MIT License - Feel free to use and modify this project.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Streamlit documentation: https://docs.streamlit.io
3. Check LangChain documentation: https://js.langchain.com

## References

- [Streamlit Documentation](https://docs.streamlit.io)
- [LangChain Documentation](https://python.langchain.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
