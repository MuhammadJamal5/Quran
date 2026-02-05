@echo off
title Quran Reel Generator
color 0b

echo =================================================
echo   Quran Reel Generator (Python 3.12 Edition)
echo =================================================
echo.

echo [1/2] Checking Dependencies (using 3.12)...
py -3.12 -m pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Could not install requirements. 
    echo Make sure Python 3.12 is installed.
    echo Trying to run anyway...
)

echo.
echo [2/2] Launching Application...
echo.
echo Opening Browser...
start http://127.0.0.1:5000

echo Running Server...
py -3.12 main.py

pause
