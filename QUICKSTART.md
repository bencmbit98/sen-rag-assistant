# Quick Start Guide

Get your RAG app running in 5 minutes!

## Step 1: Get an OpenAI API Key (5 min)

1. Go to https://platform.openai.com/api-keys
2. Sign in or create a free account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-`)
5. Keep it somewhere safe!

## Step 2: Initial Setup (2 min)

### Windows (Easiest)
1. Double-click `setup.bat`
2. Wait for it to complete
3. Edit `.env` file and paste your API key
4. Done! 🎉

### Windows PowerShell / macOS / Linux
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env  # or copy .env.example .env on Windows

# Edit .env and add your API key
# OPENAI_API_KEY=sk-your_actual_key_here
```

## Step 3: Run the App (1 min)

```bash
streamlit run app.py
```

This opens http://localhost:8501 in your browser

## Step 4: Load Documents (2-5 min)

1. Paste your OpenAI API key in the sidebar
2. Click "📖 Load Documents"
3. Wait for "✅ Documents loaded and indexed successfully!"

## Step 5: Start Asking Questions! 🚀

Try asking:
- "What are the guidelines for access arrangements?"
- "How should lecturers support HBL students?"
- "What is the student crisis support procedure?"

---

## Common Issues

### "API key not valid"
- Make sure you copied your key correctly from OpenAI
- Check for extra spaces before/after the key
- Try creating a new key if the old one is inactive

### "FAISS not found"
```bash
pip install faiss-cpu
```

### "No such file or directory: docs"
- Make sure you're in the project root directory
- The `docs` folder should be visible when you list files

### App says "No documents loaded"
- Click "📖 Load Documents" first
- Wait for the "✅ Documents loaded" message

---

## Deployment to Streamlit Cloud (10 min)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/sen-rag.git
   git push -u origin main
   ```

2. **Go to:** https://share.streamlit.io

3. **Click "New app"** and select your repo

4. **Add your API key as a secret:**
   - Click "..." → Settings
   - Go to Secrets
   - Add: `OPENAI_API_KEY = "sk-your_key"`

5. **Your app is live!** Get the public URL 🎊

---

## Next Steps

- See [README.md](README.md) for full documentation
- Customize the app by editing `app.py`
- Check [LangChain docs](https://python.langchain.com) for advanced features

Need help? Check README.md Troubleshooting section!
