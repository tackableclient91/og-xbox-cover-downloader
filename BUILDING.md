# Building Standalone Apps

This directory contains compiled standalone applications for macOS and Windows.

## macOS

The macOS .app bundle is ready to use:

```
dist/OG Xbox Cover Downloader.app
```

**To run on macOS:**

1. Double-click `OG Xbox Cover Downloader.app` in Finder
2. Or from terminal:
```bash
open dist/"OG Xbox Cover Downloader.app"
```

**Notes for macOS:**
- The app is code-signed and ready to run
- First run may ask for network permission (required to download covers)
- You may need to right-click and select "Open" if you get a security warning

## Windows

The Windows executable can be built using the provided build scripts.

### Option 1: Using Windows Command Prompt

1. Copy `BUILD_WINDOWS.bat` to your Windows machine
2. Open Command Prompt in the apps folder
3. Run: `BUILD_WINDOWS.bat`
4. The executable will be in: `dist\OG-Xbox-Cover-Downloader\OG-Xbox-Cover-Downloader.exe`

### Option 2: Using WSL/PowerShell

1. Copy `BUILD_WINDOWS.sh` to your Windows machine
2. Open PowerShell or WSL in the apps folder
3. Run: `bash BUILD_WINDOWS.sh` or `./BUILD_WINDOWS.sh`
4. The executable will be in: `dist/OG-Xbox-Cover-Downloader/`

### Option 3: Manual Build

1. Install Python 3.9+ on Windows
2. Install dependencies: `pip install -r requirements.txt`
3. Install PyInstaller: `pip install pyinstaller`
4. Run: 
```powershell
pyinstaller --name "OG-Xbox-Cover-Downloader" --onedir --windowed xbox_cover_desktop.py
```

**Requirements to build:**
- Python 3.9+
- All dependencies from `requirements.txt`
- PyInstaller

## Distribution

### macOS (.app)
- Just copy the `.app` folder/bundle
- Users can double-click to run
- Self-contained with all dependencies

### Windows (.exe)
- Entire `OG-Xbox-Cover-Downloader` folder is required
- Cannot run the .exe alone without the supporting files
- Users should extract the whole folder and run the .exe inside

## Troubleshooting

### macOS: "Cannot be opened because it is from an unidentified developer"

Right-click the app → Open (not double-click). Or use terminal:
```bash
open dist/"OG Xbox Cover Downloader.app"
```

### Windows: Missing dependencies or slow start

The first run may take a moment as all dependencies are extracted. Subsequent runs are faster.

### Both: Network permission errors

The app needs internet to download the cover index. Ensure you allow network access when prompted.
