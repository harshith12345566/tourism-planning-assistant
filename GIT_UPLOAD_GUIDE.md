# 🚀 Step-by-Step Git Upload Guide

## ⚠️ Git Not Installed

Git is not currently installed on your system. Follow these steps:

---

## Step 1: Install Git

### Option A: Download Git for Windows
1. Go to: https://git-scm.com/download/win
2. Download the installer
3. Run the installer (use default settings)
4. Restart your terminal/command prompt

### Option B: Install via Winget (Windows 11)
```powershell
winget install --id Git.Git -e --source winget
```

---

## Step 2: Configure Git (First Time Only)

After installing Git, open a new terminal and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name**: `tourism-planning-assistant`
3. **Description**: "AI-powered tourism planning web application"
4. **Visibility**: Public (or Private if you prefer)
5. **DON'T** check "Initialize with README" (we already have one)
6. Click **"Create repository"**

---

## Step 4: Upload Your Code

Open a new terminal in your project folder and run these commands:

```bash
# Navigate to your project
cd "c:\Users\harsh\OneDrive\Desktop\multi-agent inkle"

# Initialize Git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Tourism Planning Assistant with AI features"

# Add your GitHub repository as remote
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/tourism-planning-assistant.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step 5: Verify Upload

1. Go to your GitHub repository URL
2. You should see all your files uploaded
3. The README.md will be displayed automatically

---

## 🎯 Quick Commands (After Git is Installed)

Copy and paste these commands one by one:

```bash
cd "c:\Users\harsh\OneDrive\Desktop\multi-agent inkle"
git init
git add .
git commit -m "Initial commit - Tourism Planning Assistant"
git remote add origin https://github.com/YOUR_USERNAME/tourism-planning-assistant.git
git branch -M main
git push -u origin main
```

**Remember to replace `YOUR_USERNAME` with your actual GitHub username!**

---

## 🔄 Future Updates

After the initial upload, to push new changes:

```bash
git add .
git commit -m "Description of your changes"
git push origin main
```

---

## ❓ Troubleshooting

### "Git is not recognized"
- Make sure Git is installed
- Restart your terminal after installation
- Check if Git is in your PATH

### "Permission denied"
- You may need to authenticate with GitHub
- Use GitHub Desktop as an alternative
- Or set up SSH keys

### "Repository not found"
- Make sure you created the repository on GitHub
- Check that the repository name matches
- Verify your GitHub username in the URL

---

## 🎨 Alternative: GitHub Desktop (Easier)

If you prefer a GUI:

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in
3. Click "Add" → "Add Existing Repository"
4. Select your project folder
5. Click "Publish repository"
6. Done!

---

## 📝 What Gets Uploaded

✅ All your code files
✅ README.md (project documentation)
✅ DEPLOYMENT.md (deployment guide)
✅ requirements.txt (dependencies)
✅ Procfile (deployment config)
✅ Static files (CSS, JS)
✅ Templates (HTML)
✅ Agents (Python modules)

❌ __pycache__ (excluded by .gitignore)
❌ .env files (excluded by .gitignore)
❌ Virtual environment (excluded by .gitignore)

---

## 🎉 Next Steps After Upload

1. ✅ Verify files on GitHub
2. 🚀 Deploy to Render (see DEPLOYMENT.md)
3. 🌐 Share your live app URL
4. ⭐ Add a star to your own repository!

---

## 💡 Tips

- **Commit often**: Save your progress regularly
- **Write clear messages**: Describe what you changed
- **Check .gitignore**: Make sure sensitive files aren't uploaded
- **Test locally first**: Always test before pushing

---

## 🆘 Need Help?

If you encounter any issues:
1. Check the error message carefully
2. Google the error (usually has solutions)
3. Ask on Stack Overflow
4. Check GitHub's documentation

---

**Once Git is installed, come back to this guide and run the commands in Step 4!**
