# Publishing to GitHub

This guide explains how to add your OG Xbox Cover Downloader to GitHub and distribute the compiled macOS app.

## Step 1: Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Create a new repository called `og-xbox-cover-downloader`
3. Add a description: "Desktop app to download OG Xbox game covers"
4. Choose "Public" if you want others to use it freely
5. Click "Create repository"

## Step 2: Push Code to GitHub

```bash
cd /Users/asheraschilean/Desktop/apps

git init
git add .
git commit -m "Initial commit: OG Xbox Cover Downloader"
git remote add origin https://github.com/YOUR-USERNAME/og-xbox-cover-downloader.git
git branch -M main
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

## Step 3: Release the Compiled macOS App

GitHub Releases let users download the pre-built .app without needing Python.

### Create a Release

1. Go to your repository on GitHub
2. Click **Releases** (right side)
3. Click **Create a new release**
4. Fill in:
   - **Tag version:** `v1.0.0`
   - **Release title:** `OG Xbox Cover Downloader v1.0.0 - macOS`
   - **Description:**
     ```
     # OG Xbox Cover Downloader v1.0.0
     
     Pre-built macOS app (no Python needed).
     
     ## What's Included
     - Search OG Xbox game titles
     - Browse and download covers
     - Save to any folder you choose
     - Built-in retry on network errors
     
     ## How to Use
     1. Download `OG Xbox Cover Downloader.app.zip`
     2. Unzip the file
     3. Double-click the app
     4. Allow network permission if prompted
     
     ## System Requirements
     - macOS 10.15 or later
     - ARM64 (Apple Silicon) or Intel
     - Internet connection
     ```

5. **Attach the app file:**
   - Zip the app bundle first:
     ```bash
     cd /Users/asheraschilean/Desktop/apps/dist
     zip -r "OG Xbox Cover Downloader.app.zip" "OG Xbox Cover Downloader.app"
     ```
   - Drag the `OG Xbox Cover Downloader.app.zip` into the release upload area
   
6. Click **Publish release**

## Step 4: Users Can Now Download & Run

Users will see:
- Your GitHub releases page
- Download the `.app.zip` file
- Unzip it
- Double-click to run (no installation needed)

## File Structure for GitHub

Your repository should have:

```
og-xbox-cover-downloader/
├── dist/
│   └── OG Xbox Cover Downloader.app/     ← Don't commit this (too large)
├── xbox_cover_downloader.py               ← Core logic
├── xbox_cover_desktop.py                  ← Desktop GUI
├── requirements.txt                       ← Dependencies
├── README.md                              ← Main docs
├── BUILD_WINDOWS.bat                      ← Windows build script
├── BUILD_WINDOWS.sh                       ← Windows build script
└── .gitignore                             ← Excludes big files
```

## Step 5: Add .gitignore

Create a `.gitignore` file so the large compiled app doesn't get committed:

```
# Build artifacts
build/
dist/
*.spec
__pycache__/
*.pyc

# Cache
.cache/
.DS_Store

# IDE
.vscode/
.idea/
```

## Distribution Summary

**For macOS users:** They download the pre-built `.app` from your GitHub Releases page and run it directly.

**For Windows/Linux users:** They can either:
- Download the Python source and run `python3 xbox_cover_desktop.py`
- Use the build scripts to create their own exe
- Or wait for you to provide pre-built Windows releases

## Updating the Release

When you update the app:

1. Rebuild the macOS app:
   ```bash
   rm -rf build dist *.spec
   python3 -m PyInstaller --name "OG Xbox Cover Downloader" --onedir --windowed xbox_cover_desktop.py
   ```

2. Create a new GitHub release with the updated app

3. Users download the latest version from Releases

That's it! Your app is now publicly available on GitHub.
