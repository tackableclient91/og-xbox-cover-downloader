# ✅ READY TO PUSH TO GITHUB

Everything is prepared. You just need to run 3 commands:

## Step 1: Initialize Git

```bash
cd /Users/asheraschilean/Desktop/apps
git init
git add .
git commit -m "Initial commit: OG Xbox Cover Downloader"
```

## Step 2: Add GitHub Remote

Go to https://github.com/new and create a repository called `og-xbox-cover-downloader`.

Then run:

```bash
git remote add origin https://github.com/YOUR-USERNAME/og-xbox-cover-downloader.git
git branch -M main
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

## Step 3: Create Release & Push to GitHub

Use the provided script:

```bash
./push-release.sh 1.0.0
```

This will:
1. ✅ Commit changes
2. ✅ Tag version `v1.0.0`
3. ✅ Push to GitHub
4. ✅ Trigger automatic Windows build on GitHub Actions

## That's It!

In ~5 minutes:
- ✅ macOS `.app.zip` will be in the Releases
- ✅ Windows `.exe.zip` will be automatically built and added
- ✅ Users can download both as standalone executables

## What Users Get

**macOS:**
- Download `OG-Xbox-Cover-Downloader-macOS.zip` from Releases
- Unzip → Find `OG Xbox Cover Downloader.app`
- Double-click to run (no Python needed)

**Windows:**
- Download `OG-Xbox-Cover-Downloader-Windows.zip` from Releases
- Unzip → Find `OG-Xbox-Cover-Downloader.exe` inside folder
- Double-click to run (no Python needed)

## Files Ready for Commit

✅ `releases/OG-Xbox-Cover-Downloader-macOS.zip` (107 MB)  
✅ `.github/workflows/build.yml` (auto-builds Windows)  
✅ `release.sh` (script to create zips)  
✅ `push-release.sh` (one-command GitHub push)  
✅ `xbox_cover_desktop.py` (main app)  
✅ `xbox_cover_downloader.py` (downloader logic)  
✅ Documentation and guides  
✅ Updated `.gitignore`  

## Just Run These Commands:

```bash
cd /Users/asheraschilean/Desktop/apps

# Only needed once:
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/og-xbox-cover-downloader.git
git branch -M main
git push -u origin main

# For every release:
./push-release.sh 1.0.0
```

---

**Done!** Your app is now distributed on GitHub with automatic builds for both macOS and Windows.
