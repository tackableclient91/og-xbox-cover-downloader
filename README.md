# OG Xbox Game Cover Downloader

Download original Xbox game covers with ease.

Uses the public libretro thumbnail repository:
https://github.com/libretro-thumbnails/Microsoft_-_Xbox

## Download Pre-Built Apps

No Python? Download ready-to-use apps:

- **[macOS](https://github.com/tackableclient91/og-xbox-cover-downloader/releases)** - Download `OG-Xbox-Cover-Downloader-macOS.zip`, unzip, and run
- **[Windows](https://github.com/tackableclient91/og-xbox-cover-downloader/releases)** - Download `OG-Xbox-Cover-Downloader-Windows.zip`, extract, and run

Both work without needing Python!

### macOS - One-Click Setup

1. Download `OG-Xbox-Cover-Downloader-macOS.zip`
2. Unzip it
3. **Double-click `Setup-macOS.command`** (it looks like a script)
4. Done! The app will open automatically

If you see a security warning about the Setup script:
- Right-click it and choose "Open"

That's it! The setup script handles everything and launches the app.

### macOS - Manual Override (If Needed)

If the Setup script didn't work or you prefer the terminal:

**Option 1: Right-click the App**
1. Right-click "OG Xbox Cover Downloader.app"
2. Click "Open"
3. Click "Open" when prompted

**Option 2: Terminal Command**
```bash
cd ~/Downloads
unzip OG-Xbox-Cover-Downloader-macOS.zip
xattr -d com.apple.quarantine "OG Xbox Cover Downloader.app"
open "OG Xbox Cover Downloader.app"
```

## CLI Usage

```bash
python3 xbox_cover_downloader.py "Halo"
```

Downloads the best match to `covers/`.

### Options

List matches only:
```bash
python3 xbox_cover_downloader.py "Burnout" --list --max 10
```

Download all top matches:
```bash
python3 xbox_cover_downloader.py "Need for Speed" --all-matches --max 8
```

Exact matching:
```bash
python3 xbox_cover_downloader.py "Halo - Combat Evolved (USA)" --exact
```

Batch mode from file:
```bash
python3 xbox_cover_downloader.py --file games.txt --output my_covers
```

Force refresh of cached index:
```bash
python3 xbox_cover_downloader.py "Halo 2" --refresh
```

## Desktop GUI

Launch the graphical app:

```bash
python3 xbox_cover_desktop.py
```

Features:
- Search by game title
- Browse results
- Download to any folder
- Built-in retry on network issues
- Simple, clean interface

## System Requirements

- Python 3.9+ (for CLI/GUI)
- Internet connection
- No external Python packages required

## License

MIT

