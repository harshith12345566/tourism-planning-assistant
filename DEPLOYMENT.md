# 🚀 Deployment Guide - Tourism Planning Assistant

This guide will help you deploy your Tourism Planning Assistant to the cloud for free!

## 📋 Prerequisites

Before deploying, make sure you have:
- ✅ A GitHub account
- ✅ Your Gemini API key
- ✅ Git installed on your computer

---

## 🌐 Option 1: Deploy to Render (Recommended - FREE)

Render offers free hosting with automatic deployments from GitHub.

### Step 1: Push to GitHub

1. **Initialize Git** (if not already done):
```bash
cd "c:\Users\harsh\OneDrive\Desktop\multi-agent inkle"
git init
git add .
git commit -m "Initial commit - Tourism Planning Assistant"
```

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it: `tourism-planning-assistant`
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Push your code**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/tourism-planning-assistant.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Sign up/Login to Render**:
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `tourism-planning-assistant`

3. **Configure the service**:
   - **Name**: `tourism-assistant` (or any name you like)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

4. **Add Environment Variable**:
   - Click "Advanced" → "Add Environment Variable"
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key
   - Click "Add"

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your app will be live at: `https://tourism-assistant.onrender.com`

---

## 🚂 Option 2: Deploy to Railway (FREE)

Railway offers $5 free credit per month.

### Steps:

1. **Sign up at Railway**:
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add Environment Variable**:
   - Go to "Variables" tab
   - Add `GEMINI_API_KEY` with your API key

4. **Deploy**:
   - Railway auto-detects Python and deploys
   - Your app will be live at: `https://your-app.up.railway.app`

---

## ⚡ Option 3: Deploy to Vercel (Serverless)

Vercel is great for serverless deployments.

### Steps:

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Deploy**:
```bash
cd "c:\Users\harsh\OneDrive\Desktop\multi-agent inkle"
vercel
```

3. **Follow prompts**:
   - Login with GitHub
   - Set up project
   - Add `GEMINI_API_KEY` environment variable

4. **Your app will be live at**: `https://your-app.vercel.app`

---

## 🔧 Post-Deployment Configuration

### Update API Endpoints (if needed)

If your deployment URL is different from localhost, you don't need to change anything - the app uses relative URLs.

### Test Your Deployment

1. Visit your deployed URL
2. Try searching for "Paris plan my trip"
3. Check if weather and attractions load
4. Test the Save Trip feature

---

## 🐛 Troubleshooting

### App not loading?
- Check deployment logs in Render/Railway dashboard
- Verify `GEMINI_API_KEY` is set correctly
- Ensure all files are pushed to GitHub

### API errors?
- Verify your Gemini API key is valid
- Check if you have API quota remaining
- Look at server logs for specific errors

### Slow response?
- Free tier servers sleep after inactivity
- First request may take 30-60 seconds
- Subsequent requests will be faster

---

## 📊 Monitoring

### Render Dashboard
- View logs: https://dashboard.render.com
- Monitor usage and performance
- Check deployment status

### Railway Dashboard
- View logs: https://railway.app/dashboard
- Monitor credit usage
- Check metrics

---

## 🔄 Updating Your App

After making changes locally:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Render/Railway will automatically redeploy!

---

## 💡 Tips for Production

1. **Custom Domain** (Optional):
   - Buy a domain from Namecheap/GoDaddy
   - Add it in Render/Railway settings
   - Update DNS records

2. **Environment Variables**:
   - Never commit API keys to Git
   - Always use environment variables
   - Keep `.env` in `.gitignore`

3. **Monitoring**:
   - Set up uptime monitoring (UptimeRobot)
   - Enable error tracking
   - Monitor API usage

4. **Performance**:
   - Free tiers have limitations
   - Consider upgrading for production use
   - Use caching for better performance

---

## 🎉 Your App is Live!

Share your app URL with friends and family!

Example URLs:
- Render: `https://tourism-assistant.onrender.com`
- Railway: `https://tourism-assistant.up.railway.app`
- Vercel: `https://tourism-assistant.vercel.app`

---

## 📞 Need Help?

If you encounter issues:
1. Check deployment logs
2. Verify environment variables
3. Test locally first
4. Check API quotas

Happy deploying! 🚀
