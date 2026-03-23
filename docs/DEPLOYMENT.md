# Deploying Resume Screening System to Streamlit Cloud

## 🚀 Quick Deployment Guide

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

---

## Step 1: Prepare Your Repository

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Resume Screening System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/Resume_Parser_Project.git
   git push -u origin main
   ```

2. **Make sure these files are in your repo:**
   - `app.py` (Streamlit app) ✓
   - `requirements.txt` (with streamlit) ✓
   - `parsers/`, `extractors/`, `matcher/` folders ✓
   - `data/` folder with config files ✓

---

## Step 2: Deploy on Streamlit Cloud

### 2.1 Sign Up for Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "Sign up" and use your GitHub account
3. Authorize Streamlit to access your repositories

### 2.2 Deploy Your App

1. Click "New app" button
2. Fill in the details:
   - **Repository**: Select `YOUR_USERNAME/Resume_Parser_Project`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click "Deploy!"

### 2.3 Wait for Deployment

- Streamlit will install dependencies from `requirements.txt`
- First deployment takes 2-5 minutes
- You'll get a URL like: `https://your-app-name.streamlit.app`

---

## Step 3: Access Your App

Once deployed, you'll get a public URL. Share it with anyone!

**Features:**
- ✅ Upload job descriptions
- ✅ Upload 500-1000 resumes
- ✅ Get top N matches
- ✅ Download results as CSV/JSON

---

## 🔧 Configuration

### Increase Upload Limits

If you need to upload more/larger files, adjust in `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 500  # MB (adjust as needed)
```

---

## 🆓 Streamlit Cloud Limits (Free Tier)

- **1 private app** (or unlimited public apps)
- **1 GB RAM** per app
- **1 CPU** per app
- **Storage**: GitHub repository files only

**Tips:**
- For 500-1000 resumes, this should work fine
- Processing happens in batches with progress bars
- Results are generated and downloaded immediately

---

## 🔄 Updating Your App

After making changes:

```bash
git add .
git commit -m "Update description"
git push
```

Streamlit Cloud will automatically redeploy!

---

## 🐛 Troubleshooting

### App crashes during processing
- **Solution**: Reduce batch size or add more memory-efficient processing

### Upload fails
- **Solution**: Check file size limits in `config.toml`

### Dependencies not installing
- **Solution**: Make sure `requirements.txt` is correct and in root directory

---

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io

---

## Alternative: Run Locally

If you want to test before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

**Your app is now live! 🎉**
