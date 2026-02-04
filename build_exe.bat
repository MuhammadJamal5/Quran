@echo off
title Building Quran Reel Generator Executable
color 0b

echo =================================================
echo   Building Standalone EXE (Python 3.12)
echo =================================================
echo.

echo [1/2] Checking PyInstaller...
py -3.12 -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing PyInstaller...
    py -3.12 -m pip install pyinstaller
)

echo.
echo [2/2] Compiling... This may take a minute.
echo.

py -3.12 -m PyInstaller ^
 --noconfirm ^
 --onedir ^
 --console ^
 --name "QuranReelGenerator" ^
 --add-data "index.html;." ^
 --add-data "quran_text;quran_text" ^
 --add-data "fonts;fonts" ^
 --hidden-import "engineio.async_drivers.threading" ^
 --clean ^
 main.py

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Build Complete!
    echo.
    echo Your program is located in:
    echo    dist\QuranReelGenerator\QuranReelGenerator.exe
    echo.
    echo You can create a specific shortcut for that file.
) else (
    echo.
    echo [ERROR] Build Failed.
)

pause
