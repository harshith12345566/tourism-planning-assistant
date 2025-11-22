# 🚀 Quick Deployment Guide

## Fastest Way to Deploy (5 minutes)

### Option 1: Render (Recommended)

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/tourism-assistant.git
git push -u origin main
```

2. **Deploy on Render**:
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   - Add environment variable: `GEMINI_API_KEY` = `YOUR_API_KEY`
   - Click "Create Web Service"
   - Done! Your app will be live in 3-5 minutes

### Option 2: Railway

1. **Push to GitHub** (same as above)

2. **Deploy on Railway**:
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variable: `GEMINI_API_KEY`
   - Done! Live in 2-3 minutes

---

## Files Created for Deployment

✅ `Procfile` - Tells the server how to run your app
✅ `requirements.txt` - Updated with gunicorn
✅ `runtime.txt` - Specifies Python version
✅ `.gitignore` - Prevents committing sensitive files
✅ `DEPLOYMENT.md` - Full deployment guide

---

## Important Notes

⚠️ **Never commit your API key to GitHub!**
- Always use environment variables
- The `.gitignore` file protects `.env` files

✅ **Your app is production-ready!**
- All necessary files are configured
- Just push to GitHub and deploy

---

## Need Help?

Read the full `DEPLOYMENT.md` guide for detailed instructions and troubleshooting.
