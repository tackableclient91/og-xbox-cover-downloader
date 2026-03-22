#!/bin/bash

# Removes macOS security restrictions and runs the app
# Just double-click this file after unzipping!

APP_PATH="OG Xbox Cover Downloader.app"

if [ ! -d "$APP_PATH" ]; then
    echo "Error: $APP_PATH not found in this directory."
    echo "Make sure you unzipped the file correctly."
    exit 1
fi

echo "Removing security restrictions..."
xattr -rd com.apple.quarantine "$APP_PATH" 2>/dev/null || true
codesign -s - --deep --force "$APP_PATH" 2>/dev/null || true

echo "Opening app..."
open "$APP_PATH"

echo "Done! The app is now running."
