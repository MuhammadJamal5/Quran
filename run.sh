#!/usr/bin/env bash
# Quran Reel Generator — One-Click Setup (Linux / macOS)
set -e

echo "================================================="
echo "  Quran Reel Generator - One-Click Setup"
echo "================================================="
echo ""

# ── Step 1: Find or install Python ──────────────────────────────
echo "[1/4] Checking Python..."

PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo ""
    echo "  Python not found. Attempting automatic install..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &>/dev/null; then
            sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y python3 python3-pip
        elif command -v pacman &>/dev/null; then
            sudo pacman -Sy --noconfirm python python-pip
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &>/dev/null; then
            brew install python3
        else
            echo "  [ERROR] Please install Homebrew first: https://brew.sh"
            echo "  Then run this script again."
            exit 1
        fi
    fi

    # Re-check
    if command -v python3 &>/dev/null; then
        PYTHON=python3
    elif command -v python &>/dev/null; then
        PYTHON=python
    else
        echo ""
        echo "  [ERROR] Could not install Python automatically."
        echo "  Please install Python 3.9+ from https://www.python.org/downloads/"
        exit 1
    fi
fi

$PYTHON --version
echo ""

# ── Step 2: Install FFmpeg ──────────────────────────────────────
echo "[2/4] Checking FFmpeg..."

if command -v ffmpeg &>/dev/null; then
    echo "  FFmpeg found."
else
    echo ""
    echo "  FFmpeg not found. Attempting automatic install..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &>/dev/null; then
            sudo apt-get update && sudo apt-get install -y ffmpeg
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y ffmpeg
        elif command -v pacman &>/dev/null; then
            sudo pacman -Sy --noconfirm ffmpeg
        else
            echo "  [ERROR] Could not install FFmpeg automatically."
            echo "  Please install it manually for your distribution."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &>/dev/null; then
            brew install ffmpeg
        else
            echo "  [ERROR] Please install Homebrew first: https://brew.sh"
            exit 1
        fi
    fi

    if ! command -v ffmpeg &>/dev/null; then
        echo "  [ERROR] FFmpeg installation failed."
        echo "  Please install it manually."
        exit 1
    fi
    echo "  FFmpeg installed successfully."
fi
echo ""

# ── Step 3: Install Python dependencies ─────────────────────────
echo "[3/4] Installing Python dependencies..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

$PYTHON -m pip install -r "$SCRIPT_DIR/requirements.txt" --quiet 2>/dev/null || \
$PYTHON -m pip install -r "$SCRIPT_DIR/requirements.txt" --quiet --break-system-packages 2>/dev/null || \
{
    echo "  Trying with venv..."
    if [ ! -d "$SCRIPT_DIR/.venv" ]; then
        $PYTHON -m venv "$SCRIPT_DIR/.venv"
    fi
    source "$SCRIPT_DIR/.venv/bin/activate"
    pip install -r "$SCRIPT_DIR/requirements.txt" --quiet
    PYTHON="$SCRIPT_DIR/.venv/bin/python"
}

echo "  Dependencies ready."
echo ""

# ── Step 4: Launch ──────────────────────────────────────────────
echo "[4/4] Launching Quran Reel Generator..."
echo ""
echo "  The browser will open automatically when the server is ready."
echo "  (Press Ctrl+C to stop the server)"
echo ""

$PYTHON "$SCRIPT_DIR/src/main.py"
