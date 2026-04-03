@echo off
title Quran Reel Generator
color 0b

echo =================================================
echo   Quran Reel Generator
echo =================================================
echo.

:: Try to find Python (py launcher, python3, or python)
where py >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=py -3
) else (
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON=python
    ) else (
        echo [ERROR] Python not found. Please install Python 3.9+ from python.org
        pause
        exit /b 1
    )
)

echo [1/3] Checking Python...
%PYTHON% --version

echo.
echo [2/3] Installing dependencies...
%PYTHON% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Could not install all requirements.
    echo Trying to run anyway...
)

echo.
echo [3/3] Launching Application...
echo.
echo Opening browser at http://localhost:5000 ...
start http://127.0.0.1:5000

%PYTHON% src/main.py

pause
