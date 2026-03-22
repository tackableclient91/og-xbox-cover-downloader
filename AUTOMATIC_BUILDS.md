# Automatic Builds with GitHub Actions

Your project now has **automatic builds** for both macOS and Windows!

## How It Works

When you push a **git tag** to GitHub, it automatically:
1. Builds the macOS `.app`
2. Builds the Windows `.exe`
3. Creates a GitHub Release with both executables

Users can then download pre-built apps without needing Python.

## Publishing a Release

### Step 1: Push your code to GitHub

```bash
cd /Users/asheraschilean/Desktop/apps

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/og-xbox-cover-downloader.git
git branch -M main
git push -u origin main
```

### Step 2: Create a release tag and push

```bash
git tag v1.0.0
git push origin v1.0.0
```

### Step 3: Wait for builds to complete

- Go to your GitHub repository
- Click the **Actions** tab
- Watch the workflow run (takes ~5-10 minutes)
- Both builds will complete automatically

### Step 4: GitHub Release is created automatically

Once builds finish, a new release appears with:
- `OG-Xbox-Cover-Downloader-macOS.zip` (for Mac users)
- `OG-Xbox-Cover-Downloader-Windows.zip` (for Windows users)

Users can download directly from the **Releases** page!

## Updating Your App

Every time you want to release a new version:

```bash
# Make your changes, commit
git add .
git commit -m "Fix cache directory issue"

# Create a new version tag
git tag v1.0.1

# Push everything
git push
git push origin v1.0.1
```

GitHub Actions automatically builds both platforms and creates the release.

## What Gets Built

**macOS:**
- Intel and Apple Silicon compatible
- Self-contained `.app` bundle
- 67 MB compressed

**Windows:**
- Windows 10+ compatible
- Standalone `.exe` (with all dependencies)
- Run directly, no Python needed

## Requirements Files

Make sure your `.gitignore` excludes:
- `build/` - build artifacts
- `dist/` - compiled apps (too large)
- `*.spec` - PyInstaller specs

(Already set up in your repo)

## Manual Builds (if needed)

If you need to build manually on your Mac before pushing to GitHub:

```bash
# macOS
python3 -m PyInstaller --name "OG Xbox Cover Downloader" --onedir --windowed xbox_cover_desktop.py

# Then zip it
cd dist
zip -r "OG-Xbox-Cover-Downloader-macOS.zip" "OG Xbox Cover Downloader.app"
```

For Windows, use the GitHub Actions workflow or run `BUILD_WINDOWS.bat` on a Windows machine.

## Summary

✅ Push code to GitHub  
✅ Tag a release with `git tag v1.0.0`  
✅ GitHub Actions builds both macOS and Windows  
✅ Users download pre-built apps from Releases  
✅ No need for you to have Windows!
