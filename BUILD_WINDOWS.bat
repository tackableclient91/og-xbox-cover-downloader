@echo off
REM Build Windows executable using PyInstaller
REM Run this on Windows to create the .exe

cd /d "%~dp0"

echo Installing PyInstaller...
python -m pip install pyinstaller -q

echo.
echo Building Windows executable...
python -m PyInstaller ^
  --name "OG-Xbox-Cover-Downloader" ^
  --onedir ^
  --windowed ^
  xbox_cover_desktop.py

echo.
echo Build complete! Executable is in: dist\OG-Xbox-Cover-Downloader\
echo You can run it at: dist\OG-Xbox-Cover-Downloader\OG-Xbox-Cover-Downloader.exe

pause
