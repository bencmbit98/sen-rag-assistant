# Deployment Guide - Streamlit Cloud

This guide walks you through deploying your SEN RAG Assistant to Streamlit Cloud.

## Prerequisites

- GitHub account (free at https://github.com)
- Your project pushed to GitHub
- OpenAI API key (obtained from https://platform.openai.com/api-keys)

---

## Step 1: Prepare Your Project for GitHub

### 1.1 Initialize Git (if not already done)

```bash
git init
```

### 1.2 Create a `.gitignore` file

Already included in the project! It excludes:
- `.env` (sensitive API keys)
- `venv/` and `env/` (virtual environments)
- `faiss_index/` (regenerated on first run)
- `__pycache__/` (Python cache files)

### 1.3 Commit Your Files

```bash
git add .
git commit -m "Initial commit: SEN RAG Assistant"
```

### 1.4 Check Your Git Status

```bash
git status
```

You should see your files staged and ready to push. ✓

---

## Step 2: Push to GitHub

### 2.1 Create a New Repository on GitHub

1. Go to https://github.com/new
2. Name it `sen-rag-assistant` (or any name you prefer)
3. Add description: "RAG LLM App for SEN Guidelines"
4. Click "Create repository"
5. **DO NOT initialize with README** (you already have one)

### 2.2 Add Remote and Push

Copy the HTTPS URL from GitHub (looks like `https://github.com/your-username/sen-rag-assistant.git`)

```bash
# Add remote
git remote add origin https://github.com/your-username/sen-rag-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2.3 Verify

Go to your GitHub repository URL and verify all files are there!

---

## Step 3: Deploy on Streamlit Cloud

### 3.1 Go to Streamlit Cloud

1. Visit https://share.streamlit.io
2. Sign in with your GitHub account (create if needed)
3. Click "New app"

### 3.2 Connect Your Repository

1. Select your GitHub account
2. Select repository: `sen-rag-assistant`
3. Select branch: `main`
4. Set main file path: `app.py`
5. Click "Deploy"

Streamlit will now:
- Clone your repository
- Install dependencies from `requirements.txt`
- Run your app
- Provide a public URL

This takes ~2-3 minutes for the first deploy.

---

## Step 4: Add Your OpenAI API Key

**IMPORTANT:** Never commit your API key to GitHub!

### 4.1 Access App Settings

1. On your deployed app, click the "..." menu (top right)
2. Click "Settings"
3. Click the "Secrets" tab on the left

### 4.2 Add Your API Key

In the "Secrets" text area, add:

```
OPENAI_API_KEY = "sk-your_actual_api_key_here"
```

- Click "Save"
- Your app will automatically reboot with the secret loaded

### 4.3 Verify

1. Paste your OpenAI API key in the sidebar
2. Click "📖 Load Documents"
3. If it works, your app is ready! 🎉

---

## Step 5: Share Your App

Your app is now live! The URL looks like:
```
https://sen-rag-assistant-username.streamlit.app
```

Share this URL with anyone who needs access. They can start using it immediately!

---

## Updating Your App

### Make Local Changes

1. Edit `app.py` or other files
2. Test locally: `streamlit run app.py`
3. Commit and push:
   ```bash
   git add .
   git commit -m "Add feature: X"
   git push origin main
   ```

### Streamlit Cloud Auto-Redeploys

- Streamlit Cloud automatically detects your push
- Your app redeployss within 1-2 minutes
- No manual action needed!

---

## Troubleshooting Deployment

### App Shows "Failed to start"

**Problem:** Dependencies not installed properly

**Solution:**
- Check `requirements.txt` for syntax errors
- Run `pip install -r requirements.txt` locally to verify
- Commit and push for a redeploy

### "FileNotFoundError: docs folder"

**Problem:** docs folder not in GitHub

**Solution:**
```bash
# Add docs folder to git
git add docs/
git commit -m "Add docs"
git push
```

### API Key Not Working

**Problem:** Secrets not configured

**Solution:**
1. Go to app Settings → Secrets
2. Add: `OPENAI_API_KEY = "sk-..."`
3. Save and wait for reboot (~1 min)
4. Try again

### App is Slow

**Problem:** FAISS index being rebuilt on each startup

**Solution:**
- First startup will take 2-5 minutes
- Subsequent startups use cached index (faster)
- If still slow, upgrade your Streamlit Cloud plan

### "No module named 'langchain'"

**Problem:** Dependency not installed

**Solution:**
1. Verify `requirements.txt` has all packages
2. Run locally: `pip install -r requirements.txt`
3. Verify no errors
4. Commit and push

---

## Advanced Deployment Options

### A. Docker Deployment

For more control, deploy with Docker:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Platforms: Railway, Render, Heroku, AWS

### B. Self-Hosted Deployment

Deploy your own server:

```bash
# On your server
git clone https://github.com/your-username/sen-rag-assistant.git
cd sen-rag-assistant
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Add .env with API key
streamlit run app.py --server.port=8501
```

Then access at: `http://your-server-ip:8501`

### C. Serverless (AWS Lambda, Google Cloud Functions)

Not recommended for this app because:
- Long processing time on first load
- Large dependencies
- API calls need to complete

---

## Cost Considerations

### Streamlit Cloud
- Free tier: Up to 1 GB memory per app
- Community cloud: Free deployment
- Professional plans: ~$10/month for more resources

### OpenAI Costs
- Every API call costs money
- Embeddings: ~$0.01 per 1M tokens (during load)
- GPT-4: ~$0.09 per question (can vary)
- Estimate: $5-20/month for moderate usage

### Cost Optimization
1. Use GPT-3.5-turbo instead of GPT-4 (3x cheaper)
2. Reduce `chunk_size` for faster processing
3. Cache vector store (already implemented)
4. Limit number of retrieved documents

---

## Monitoring & Logs

### View Deployment Logs

1. Go to https://share.streamlit.io
2. Click your app
3. Click "Manage app" → "Logs"

Look for:
- `WARNING`: Potential issues
- `ERROR`: Failed operations
- `INFO`: Normal operation

### Set Up Alerts

Streamlit Cloud doesn't have built-in alerts, but you can:
1. Monitor API usage on OpenAI dashboard
2. Set up GitHub notifications for repo changes
3. Regularly check the logs

---

## Support & Resources

- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-cloud
- Deployment FAQs: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/app-dependencies
- LangChain Docs: https://python.langchain.com
- OpenAI Docs: https://platform.openai.com/docs

---

## Next Steps

✅ Your app is deployed!

Now consider:
- [ ] Customize the UI colors in `.streamlit/config.toml`
- [ ] Add more documents to `docs/` folder
- [ ] Experiment with different models
- [ ] Share with your team!

Happy deploying! 🚀
