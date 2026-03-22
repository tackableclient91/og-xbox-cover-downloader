#!/bin/bash
# Quick launcher for the macOS app

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_PATH="$SCRIPT_DIR/dist/OG Xbox Cover Downloader.app"

if [ -d "$APP_PATH" ]; then
    echo "Launching OG Xbox Cover Downloader..."
    open "$APP_PATH"
else
    echo "Error: App not found at $APP_PATH"
    echo "Please run: python3 -m PyInstaller --name 'OG Xbox Cover Downloader' --onedir --windowed xbox_cover_desktop.py"
    exit 1
fi
