#!/usr/bin/env bash
# Quran Reel Generator — Cross-platform launcher (Linux / macOS)
set -e

echo "================================================="
echo "  Quran Reel Generator"
echo "================================================="
echo ""

# Find Python 3
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "[ERROR] Python not found. Please install Python 3.9+"
    exit 1
fi

echo "[1/3] Checking Python..."
$PYTHON --version

echo ""
echo "[2/3] Installing dependencies..."
$PYTHON -m pip install -r requirements.txt

# Check for ffmpeg
if ! command -v ffmpeg &>/dev/null; then
    echo ""
    echo "[WARNING] ffmpeg not found!"
    echo "  Install it with:"
    echo "    Ubuntu/Debian: sudo apt install ffmpeg"
    echo "    macOS:         brew install ffmpeg"
    echo "    Fedora:        sudo dnf install ffmpeg"
    echo ""
fi

echo ""
echo "[3/3] Launching Application..."
echo ""
echo "  Open http://localhost:5000 in your browser"
echo ""

# Try to open browser (non-blocking, ignore errors)
if command -v xdg-open &>/dev/null; then
    xdg-open http://localhost:5000 &>/dev/null &
elif command -v open &>/dev/null; then
    open http://localhost:5000 &>/dev/null &
fi

$PYTHON src/main.py
