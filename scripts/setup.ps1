# Quick Start Guide - Quran Cinematic Reels Generator

Write-Host "`n" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  Quran Cinematic Reels Generator - Quick Start" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor White
    exit 1
}

# Check FFmpeg
Write-Host "`n[2/5] Checking FFmpeg installation..." -ForegroundColor Yellow
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "   ✓ FFmpeg found" -ForegroundColor Green
} catch {
    Write-Host "   ✗ FFmpeg not found!" -ForegroundColor Red
    Write-Host "   Please install FFmpeg and add to PATH" -ForegroundColor White
    Write-Host "   Download from: https://ffmpeg.org/download.html" -ForegroundColor White
    $continue = Read-Host "`n   Continue anyway? (y/n)"
    if ($continue -ne "y") { exit 1 }
}

# Install Python packages
Write-Host "`n[3/5] Installing Python packages..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor White
try {
    pip install -r requirements.txt --quiet
    Write-Host "   ✓ All packages installed" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ Some packages may have failed to install" -ForegroundColor Yellow
}

# Download fonts (optional)
Write-Host "`n[4/5] Do you want to download Quranic fonts?" -ForegroundColor Yellow
Write-Host "   (Recommended for better text quality)" -ForegroundColor White
$downloadFonts = Read-Host "   Download fonts? (y/n)"
if ($downloadFonts -eq "y") {
    .\download_fonts.ps1
}

# Check directories
Write-Host "`n[5/5] Checking project structure..." -ForegroundColor Yellow
$dirs = @("audio", "outputs", "backgrounds", "fonts", "temp")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Write-Host "   ✓ $dir/" -ForegroundColor Green
}

# Summary
Write-Host "`n=====================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the server, run:" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Then open your browser at:" -ForegroundColor White
Write-Host "   http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan

$startNow = Read-Host "`nStart the server now? (y/n)"
if ($startNow -eq "y") {
    Write-Host "`nStarting server..." -ForegroundColor Green
    python main.py
}
