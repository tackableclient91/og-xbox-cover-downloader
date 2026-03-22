# Quick Start: Release to GitHub

## TL;DR

Get both macOS and Windows executables without needing Windows:

```bash
# 1. Initialize git
cd /Users/asheraschilean/Desktop/apps
git init
git add .
git commit -m "Initial commit"

# 2. Create GitHub repo at https://github.com/new
# Then:
git remote add origin https://github.com/YOUR-USERNAME/og-xbox-cover-downloader.git
git branch -M main
git push -u origin main

# 3. Create a release
git tag v1.0.0
git push origin v1.0.0

# 4. GitHub Actions builds both platforms automatically (~5 min)
# Release appears at: https://github.com/YOUR-USERNAME/og-xbox-cover-downloader/releases
```

## That's It!

Users download:
- **macOS**: `OG-Xbox-Cover-Downloader-macOS.zip` → unzip → double-click
- **Windows**: `OG-Xbox-Cover-Downloader-Windows.zip` → unzip → run `.exe`

No Python needed. Works out of the box.

## What Happens After You Push

1. GitHub detects the `v1.0.0` tag
2. Automatically starts build workflow
3. macOS runner builds the `.app`
4. Windows runner builds the `.exe`
5. Both get zipped and attached to a Release
6. Users can download from Releases page

## Updating the App

```bash
git add .
git commit -m "Your changes"
git tag v1.0.1
git push
git push origin v1.0.1
```

Same thing - automatic builds for both platforms.

## Where to Find Files

After pushing to GitHub:
- Go to your repo
- Click **Releases** tab
- Download `.zip` files for macOS or Windows

Done! Your app is distributed.

---

For detailed instructions, see [AUTOMATIC_BUILDS.md](AUTOMATIC_BUILDS.md)
