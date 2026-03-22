#!/bin/bash
# Release script - zips both macOS and Windows apps
# Run this before pushing to GitHub to create release artifacts

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIST_DIR="$SCRIPT_DIR/dist"
RELEASES_DIR="$SCRIPT_DIR/releases"

echo "🚀 OG Xbox Cover Downloader - Release Builder"
echo ""

# Create releases directory
mkdir -p "$RELEASES_DIR"
rm -f "$RELEASES_DIR"/*.zip

echo "📦 Preparing release files..."
echo ""

# Check if macOS app exists
if [ -d "$DIST_DIR/OG Xbox Cover Downloader.app" ]; then
    echo "✓ Found macOS app"
    
    # Create macOS zip
    cd "$DIST_DIR"
    zip -r -q "../releases/OG-Xbox-Cover-Downloader-macOS.zip" "OG Xbox Cover Downloader.app"
    cd - > /dev/null
    
    SIZE=$(du -sh "$RELEASES_DIR/OG-Xbox-Cover-Downloader-macOS.zip" | cut -f1)
    echo "  → Zipped: releases/OG-Xbox-Cover-Downloader-macOS.zip ($SIZE)"
else
    echo "✗ macOS app not found. Run PyInstaller first:"
    echo "  python3 -m PyInstaller --name 'OG Xbox Cover Downloader' --onedir --windowed xbox_cover_desktop.py"
    exit 1
fi

echo ""
echo "✅ Release files ready in: releases/"
echo ""
echo "📋 What to do next:"
echo ""
echo "  1. Commit your changes:"
echo "     git add ."
echo "     git commit -m 'Release version X.X.X'"
echo ""
echo "  2. Create a release tag:"
echo "     git tag v1.0.0"
echo ""
echo "  3. Push to GitHub:"
echo "     git push origin main"
echo "     git push origin v1.0.0"
echo ""
echo "  4. GitHub Actions will automatically:"
echo "     - Build Windows .exe"
echo "     - Create a Release with both macOS and Windows files"
echo ""
echo "📌 Note: GitHub Actions will build Windows automatically."
echo "   You don't need to build it on your Mac!"
echo ""
