#!/bin/bash
# Build Windows executable using PyInstaller on Windows/WSL

cd "$(dirname "$0")"

echo "Installing PyInstaller..."
python3 -m pip install pyinstaller -q

echo ""
echo "Building Windows executable..."
python3 -m PyInstaller \
  --name "OG-Xbox-Cover-Downloader" \
  --onedir \
  --windowed \
  xbox_cover_desktop.py

echo ""
echo "Build complete! Executable is in: dist/OG-Xbox-Cover-Downloader/"
echo "You can run it at: dist/OG-Xbox-Cover-Downloader/OG-Xbox-Cover-Downloader.exe"
