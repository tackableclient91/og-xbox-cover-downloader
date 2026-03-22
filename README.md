# OG Xbox Game Cover Downloader

CLI tool to search and download original Xbox game covers.

It uses the public libretro thumbnail repository as the image source:
- https://github.com/libretro-thumbnails/Microsoft_-_Xbox

## Requirements

- Python 3.9+
- Internet connection

No third-party Python packages are required.

## Quick Start

```bash
python3 xbox_cover_downloader.py "Halo"
```

Downloads the best match into `covers/`.

## Useful Commands

List matches only:

```bash
python3 xbox_cover_downloader.py "Burnout" --list --max 10
```

Download all top matches instead of only the best one:

```bash
python3 xbox_cover_downloader.py "Need for Speed" --all-matches --max 8
```

Use exact matching:

```bash
python3 xbox_cover_downloader.py "Halo - Combat Evolved (USA)" --exact
```

Batch mode from file (`games.txt`, one title per line):

```bash
python3 xbox_cover_downloader.py --file games.txt --output my_covers
```

Force refresh of cached index:

```bash
python3 xbox_cover_downloader.py "Halo 2" --refresh
```

## Notes

- The cover index is cached in `.cache/xbox_cover_index.json` for 24 hours.
- Region tags like `(USA)` and `(Europe)` are used for tie-breaking by default.
- You can customize region preference with `--region-order`.

## Desktop App

The project includes a fully functional desktop app for easy searching and downloading.

Install GUI dependency:

```bash
python3 -m pip install -r requirements.txt
```

Launch the app:

```bash
python3 xbox_cover_desktop.py
```

Desktop app features:

- Search OG Xbox games by title
- Browse and select results from the list
- Click "Download Selected" to download the chosen cover
- Choose any download folder with the "Browse" button (defaults to Downloads)
- Built-in status log shows search results and download progress
- Automatic network retry on transient failures
- Simple, clean interface focused on core functionality
