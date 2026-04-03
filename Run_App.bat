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
set "FFMPEG_APPDIR=%LOCALAPPDATA%\QuranReelGenerator"
set "FFMPEG_DIR=%FFMPEG_APPDIR%\ffmpeg"

where ffmpeg >nul 2>&1
if %errorlevel% equ 0 (
    echo  FFmpeg found on system PATH.
    goto :ffmpeg_ready
)

:: Check persistent local install
if exist "%FFMPEG_DIR%\ffmpeg.exe" (
    set "PATH=%FFMPEG_DIR%;%PATH%"
    echo  Using previously downloaded FFmpeg.
    goto :ffmpeg_ready
)

echo.
echo  FFmpeg not found. Downloading once (will be reused on future runs)...
echo.

:: Create persistent directory
if not exist "%FFMPEG_APPDIR%" mkdir "%FFMPEG_APPDIR%"
if not exist "%FFMPEG_DIR%" mkdir "%FFMPEG_DIR%"

:: Download ffmpeg essentials (much smaller than full GPL build)
set "FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
set "FFMPEG_ZIP=%FFMPEG_APPDIR%\ffmpeg_download.zip"

powershell -NoProfile -Command ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " ^
    "Write-Host '  Downloading FFmpeg essentials...'; " ^
    "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile '%FFMPEG_ZIP%' -UseBasicParsing"

if not exist "%FFMPEG_ZIP%" (
    echo.
    echo  [ERROR] FFmpeg download failed.
    echo  Please download FFmpeg manually from: https://www.gyan.dev/ffmpeg/builds/
    echo  Extract ffmpeg.exe and ffprobe.exe into: %FFMPEG_DIR%
    pause
    exit /b 1
)

:: Extract ONLY the bin/ folder (ffmpeg.exe, ffprobe.exe, ffplay.exe) to save space
echo  Extracting FFmpeg (bin only)...
powershell -NoProfile -Command ^
    "Add-Type -Assembly System.IO.Compression.FileSystem; " ^
    "$zip = [IO.Compression.ZipFile]::OpenRead('%FFMPEG_ZIP%'); " ^
    "try { " ^
    "  foreach ($entry in $zip.Entries) { " ^
    "    if ($entry.FullName -match '/bin/[^/]+\.exe$') { " ^
    "      $name = [IO.Path]::GetFileName($entry.FullName); " ^
    "      $dest = Join-Path '%FFMPEG_DIR%' $name; " ^
    "      [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $dest, $true); " ^
    "      Write-Host ('  Extracted: ' + $name); " ^
    "    } " ^
    "  } " ^
    "} finally { $zip.Dispose() }; " ^
    "Remove-Item '%FFMPEG_ZIP%' -Force -ErrorAction SilentlyContinue"

if exist "%FFMPEG_DIR%\ffmpeg.exe" (
    set "PATH=%FFMPEG_DIR%;%PATH%"
    echo  FFmpeg installed successfully.
    echo  (Saved to %FFMPEG_DIR% - won't download again)
) else (
    echo.
    echo  [ERROR] FFmpeg extraction failed. You may be low on disk space.
    echo  Please download FFmpeg manually from: https://www.gyan.dev/ffmpeg/builds/
    echo  Extract ffmpeg.exe and ffprobe.exe into: %FFMPEG_DIR%
    :: Clean up failed download
    del "%FFMPEG_ZIP%" >nul 2>&1
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
