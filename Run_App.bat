@echo off
title Quran Reel Generator
color 0b

echo =================================================
echo   Quran Reel Generator - One-Click Setup
echo =================================================
echo.

:: ── Step 1: Find or Install Python ──────────────────────────────
echo [1/4] Checking Python...

set PYTHON=
where py >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=py -3
    goto :found_python
)
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=python
    goto :found_python
)

echo.
echo  Python is not installed. Attempting automatic install...
echo.

:: Try winget first (Windows 10 1709+ / Windows 11)
where winget >nul 2>&1
if %errorlevel% equ 0 (
    echo  Installing Python via winget...
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    if %errorlevel% equ 0 (
        echo.
        echo  Python installed! Restarting setup...
        echo  Please close this window and double-click Run_App.bat again.
        pause
        exit /b 0
    )
)

echo.
echo ====================================================
echo  [ERROR] Could not install Python automatically.
echo.
echo  Please download Python from:
echo    https://www.python.org/downloads/
echo.
echo  IMPORTANT: Check "Add Python to PATH" during install!
echo ====================================================
echo.
pause
exit /b 1

:found_python
%PYTHON% --version
echo.

:: ── Step 2: Install FFmpeg ──────────────────────────────────────
echo [2/4] Checking FFmpeg...

:: Persistent location that survives re-downloading the project ZIP
set "FFMPEG_DIR=%LOCALAPPDATA%\QuranReelGenerator\ffmpeg"

where ffmpeg >nul 2>&1
if %errorlevel% equ 0 (
    echo  FFmpeg found on system PATH.
    goto :ffmpeg_ready
)

:: Check persistent local install
if exist "%FFMPEG_DIR%\bin\ffmpeg.exe" (
    set "PATH=%FFMPEG_DIR%\bin;%PATH%"
    echo  Using previously downloaded FFmpeg.
    goto :ffmpeg_ready
)

echo.
echo  FFmpeg not found. Downloading once (will be reused on future runs)...
echo.

:: Create persistent directory
if not exist "%LOCALAPPDATA%\QuranReelGenerator" mkdir "%LOCALAPPDATA%\QuranReelGenerator"

:: Download ffmpeg using PowerShell
set "FFMPEG_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
set "FFMPEG_ZIP=%LOCALAPPDATA%\QuranReelGenerator\ffmpeg_download.zip"

powershell -NoProfile -Command ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " ^
    "Write-Host '  Downloading FFmpeg (this may take a minute)...'; " ^
    "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile '%FFMPEG_ZIP%' -UseBasicParsing"

if not exist "%FFMPEG_ZIP%" (
    echo.
    echo  [ERROR] FFmpeg download failed.
    echo  Please download FFmpeg manually from: https://ffmpeg.org/download.html
    pause
    exit /b 1
)

echo  Extracting FFmpeg...
powershell -NoProfile -Command ^
    "$tempDir = '%LOCALAPPDATA%\QuranReelGenerator\ffmpeg_temp'; " ^
    "Expand-Archive -Path '%FFMPEG_ZIP%' -DestinationPath $tempDir -Force; " ^
    "$extracted = Get-ChildItem $tempDir -Directory | Select-Object -First 1; " ^
    "if ($extracted) { " ^
    "  if (Test-Path '%FFMPEG_DIR%') { Remove-Item '%FFMPEG_DIR%' -Recurse -Force }; " ^
    "  Move-Item $extracted.FullName '%FFMPEG_DIR%' " ^
    "}; " ^
    "Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue; " ^
    "Remove-Item '%FFMPEG_ZIP%' -Force -ErrorAction SilentlyContinue"

if exist "%FFMPEG_DIR%\bin\ffmpeg.exe" (
    set "PATH=%FFMPEG_DIR%\bin;%PATH%"
    echo  FFmpeg installed successfully.
    echo  (Saved to %FFMPEG_DIR% - won't download again)
) else (
    echo.
    echo  [ERROR] FFmpeg extraction failed.
    echo  Please download FFmpeg manually from: https://ffmpeg.org/download.html
    pause
    exit /b 1
)

:ffmpeg_ready
echo.

:: ── Step 3: Install Python Dependencies ─────────────────────────
echo [3/4] Installing Python dependencies...
%PYTHON% -m pip install --upgrade pip >nul 2>&1
%PYTHON% -m pip install -r "%~dp0requirements.txt"
if %errorlevel% neq 0 (
    echo.
    echo  [WARNING] Some packages failed. Installing one by one...
    for /f "usebackq delims=" %%p in ("%~dp0requirements.txt") do (
        %PYTHON% -m pip install %%p
    )
)
echo  Dependencies ready.
echo.

:: ── Step 4: Launch ──────────────────────────────────────────────
echo [4/4] Launching Quran Reel Generator...
echo.
echo  The browser will open automatically when the server is ready.
echo  (Close this window to stop the server)
echo.

%PYTHON% "%~dp0src\main.py"

pause
