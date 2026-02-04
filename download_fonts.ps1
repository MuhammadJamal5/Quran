# Font Download Helper for Quran Reels Generator

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "  Quran Fonts Downloader" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$fontsDir = ".\fonts"

if (-not (Test-Path $fontsDir)) {
    New-Item -ItemType Directory -Path $fontsDir | Out-Null
    Write-Host "`n✓ Created fonts directory" -ForegroundColor Green
}

Write-Host "`nDownloading Quran fonts...`n" -ForegroundColor Yellow

# Amiri Font
Write-Host "1. Downloading Amiri (Arabic Font)..." -ForegroundColor White
try {
    $amiriUrl = "https://github.com/aliftype/amiri/releases/download/0.113/Amiri-0.113.zip"
    $amiriZip = "$fontsDir\amiri.zip"
    
    Invoke-WebRequest -Uri $amiriUrl -OutFile $amiriZip -UseBasicParsing
    Expand-Archive -Path $amiriZip -DestinationPath "$fontsDir\amiri_temp" -Force
    
    # Find and copy TTF files
    Get-ChildItem -Path "$fontsDir\amiri_temp" -Filter "*.ttf" -Recurse | ForEach-Object {
        Copy-Item $_.FullName -Destination $fontsDir
    }
    
    Remove-Item $amiriZip
    Remove-Item "$fontsDir\amiri_temp" -Recurse -Force
    
    Write-Host "   ✓ Amiri font installed" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Failed to download Amiri" -ForegroundColor Red
}

# Scheherazade Font
Write-Host "`n2. Downloading Scheherazade (Quranic Font)..." -ForegroundColor White
try {
    $scheherazadeUrl = "https://github.com/silnrsi/font-scheherazade/releases/download/v3.300/ScheherazadeNew-3.300.zip"
    $scheherazadeZip = "$fontsDir\scheherazade.zip"
    
    Invoke-WebRequest -Uri $scheherazadeUrl -OutFile $scheherazadeZip -UseBasicParsing
    Expand-Archive -Path $scheherazadeZip -DestinationPath "$fontsDir\scheherazade_temp" -Force
    
    Get-ChildItem -Path "$fontsDir\scheherazade_temp" -Filter "*.ttf" -Recurse | ForEach-Object {
        Copy-Item $_.FullName -Destination $fontsDir
    }
    
    Remove-Item $scheherazadeZip
    Remove-Item "$fontsDir\scheherazade_temp" -Recurse -Force
    
    Write-Host "   ✓ Scheherazade font installed" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Failed to download Scheherazade" -ForegroundColor Red
}

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "  Installation Summary" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$installedFonts = Get-ChildItem -Path $fontsDir -Filter "*.ttf"
if ($installedFonts.Count -gt 0) {
    Write-Host "`n✓ Installed fonts:" -ForegroundColor Green
    foreach ($font in $installedFonts) {
        Write-Host "  - $($font.Name)" -ForegroundColor White
    }
} else {
    Write-Host "`n! No fonts were installed" -ForegroundColor Yellow
    Write-Host "  The app will use system fonts (arial.ttf)" -ForegroundColor Yellow
}

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "`nNote: Windows users can also use:" -ForegroundColor Yellow
Write-Host "  Traditional Arabic Bold (TRADBDO.TTF)" -ForegroundColor White
Write-Host "  This font is already available in Windows`n" -ForegroundColor White

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
