Write-Host "Building Project..." -ForegroundColor Cyan
py -3.12 -m PyInstaller --noconfirm --onedir --console --name "QuranReelGenerator" --add-data "index.html;." --add-data "quran_text;quran_text" --add-data "fonts;fonts" --hidden-import "engineio.async_drivers.threading" --clean main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build Successful. Zipping..." -ForegroundColor Green
    $source = "dist\QuranReelGenerator"
    $destination = "QuranReelGenerator.zip"
    if (Test-Path $destination) { Remove-Item $destination }
    Compress-Archive -Path $source -DestinationPath $destination
    Write-Host "Created $destination" -ForegroundColor Green
} else {
    Write-Host "Build Failed" -ForegroundColor Red
}
