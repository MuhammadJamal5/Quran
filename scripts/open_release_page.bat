@echo off
echo Opening GitHub Releases Page...
start https://github.com/MuhammadJamal5/Quran/releases/new

echo Opening Output Folder...
explorer /select, "c:\Quran\QuranReelGenerator.zip"

echo ========================================================
echo Instructions:
echo 1. In the browser window, add a tag (e.g., v1.0).
echo 2. Drag 'QuranReelGenerator.zip' from the folder into the upload box.
echo 3. Click 'Publish release'.
echo ========================================================
pause
