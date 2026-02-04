@echo off
title Quran Reel Generator
cd /d "%~dp0"

:: Check for Python
python --version >NUL 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

:: Check for ALL critical dependencies
python -c "import flask, requests, PIL, pydub, arabic_reshaper, bidi" >NUL 2>&1
if %errorlevel% neq 0 (
    echo [INFO] First time setup: Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install packages. Check your internet connection.
        pause
        exit /b
    )
    cls
)

cls
echo =====================================================
echo   Quran Reel Generator is running...
echo =====================================================
echo.
echo [INFO] Starting server...
echo [INFO] Opening browser...
echo.
echo Please keep this window open while using the app.
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] An error occurred!
    echo.
    pause
)
