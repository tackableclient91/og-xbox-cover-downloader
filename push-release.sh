#!/bin/bash
# Quick push to GitHub with automatic Windows build

if [ $# -lt 1 ]; then
    echo "Usage: $0 <version>"
    echo ""
    echo "Example: $0 1.0.0"
    echo ""
    echo "This will:"
    echo "  1. Commit changes"
    echo "  2. Tag version v1.0.0"
    echo "  3. Push to GitHub"
    echo "  4. GitHub Actions automatically builds Windows .exe"
    exit 1
fi

VERSION="$1"
TAG="v$VERSION"

echo "🚀 Pushing to GitHub with automatic Windows build..."
echo ""

# Make sure we have a git repo
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Run git init first."
    exit 1
fi

# Commit
echo "📝 Committing changes..."
git add .
git commit -m "Release v$VERSION" || echo "   (nothing to commit)"

# Tag
echo "🏷️  Creating tag $TAG..."
git tag -d "$TAG" 2>/dev/null || true
git tag "$TAG"

# Push
echo "📤 Pushing to GitHub..."
git push origin main || git push -u origin main
git push origin "$TAG"

echo ""
echo "✅ Pushed to GitHub!"
echo ""
echo "⏳ GitHub Actions is now building Windows automatically..."
echo "   Check: https://github.com/YOUR-USERNAME/og-xbox-cover-downloader/actions"
echo ""
echo "📥 In ~5 minutes, releases will be available at:"
echo "   https://github.com/YOUR-USERNAME/og-xbox-cover-downloader/releases"
echo ""
