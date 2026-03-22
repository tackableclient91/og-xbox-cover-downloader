# OG Xbox Cover Downloader - Compiled Apps Ready

Both standalone applications have been compiled and are ready to use.

## 📦 macOS App (Ready to Use)

**Location:** `dist/OG Xbox Cover Downloader.app`  
**Size:** ~67 MB  
**Status:** ✅ Ready to run immediately

To launch:
```bash
open dist/"OG Xbox Cover Downloader.app"
```

Or just double-click the app in Finder.

## 🪟 Windows App

Two options to get the Windows executable:

### Option A: Pre-built (Coming Soon)
Windows .exe will be available in the `dist/` folder once built on a Windows machine.

### Option B: Build It Yourself
Use the provided build scripts:

**On Windows (Command Prompt):**
```bash
BUILD_WINDOWS.bat
```

**On Windows (PowerShell) or WSL:**
```bash
bash BUILD_WINDOWS.sh
```

**Manually:**
```bash
pip install pyinstaller
pyinstaller --name "OG-Xbox-Cover-Downloader" --onedir --windowed xbox_cover_desktop.py
```

For detailed instructions, see [BUILDING.md](BUILDING.md)

## 📋 Requirements to Build

**For macOS (already done):**
- Python 3.9+
- PySide6
- PyInstaller (installed automatically)

**For Windows (to build):**
- Python 3.9+ (Windows)
- PySide6
- PyInstaller

## 🚀 What's Included

- **Desktop GUI** with search and download functionality
- **Automatic retries** for network failures
- **Folder selection** - save covers anywhere you want
- **Status logging** - see what's happening in real-time
- **Zero configuration** - works right out of the box

## 🔧 Building New Versions

If you modify the Python source code:

**macOS:**
```bash
python3 -m PyInstaller --name "OG Xbox Cover Downloader" --onedir --windowed xbox_cover_desktop.py
```

**Windows:**
```bash
python -m PyInstaller --name "OG-Xbox-Cover-Downloader" --onedir --windowed xbox_cover_desktop.py
```

## 📝 File Structure

```
apps/
├── dist/
│   └── OG Xbox Cover Downloader.app/     ← macOS executable (ready)
├── xbox_cover_downloader.py               ← Core downloader logic
├── xbox_cover_desktop.py                  ← Desktop GUI source
├── BUILD_WINDOWS.bat                      ← Windows build script
├── BUILD_WINDOWS.sh                       ← Windows/WSL build script
├── BUILDING.md                            ← Detailed build guide
├── README.md                              ← Main project docs
└── requirements.txt                       ← Python dependencies
```

## ✨ Next Steps

1. **macOS users:** Run the app with `open dist/"OG Xbox Cover Downloader.app"`
2. **Windows users:** Use one of the build scripts to create the .exe
3. **Both:** Enjoy downloading OG Xbox game covers!
