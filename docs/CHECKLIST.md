# ✅ Quran Cinematic Reels Generator - Installation Checklist

## 📋 Pre-Installation Checklist

### System Requirements
- [ ] Windows 10 or later
- [ ] PowerShell 5.1 or later
- [ ] Internet connection (for initial setup)
- [ ] At least 1 GB free disk space

### Software Requirements
- [ ] Python 3.8+ installed
  ```powershell
  python --version
  # Should show: Python 3.8.x or higher
  ```

- [ ] pip installed (comes with Python)
  ```powershell
  pip --version
  # Should show pip version
  ```

- [ ] FFmpeg installed and in PATH
  ```powershell
  ffmpeg -version
  # Should show FFmpeg version
  ```

---

## 🔧 Installation Checklist

### Step 1: Download/Clone Project
- [ ] Project files downloaded to C:\Quran (or your preferred location)
- [ ] All files present:
  - [ ] main.py
  - [ ] index.html
  - [ ] requirements.txt
  - [ ] setup.ps1
  - [ ] download_fonts.ps1
  - [ ] test_generator.py
  - [ ] README.md
  - [ ] Other documentation files

### Step 2: Run Setup Script
- [ ] Open PowerShell in project directory
  ```powershell
  cd C:\Quran
  ```

- [ ] Run setup script
  ```powershell
  .\setup.ps1
  ```

- [ ] Setup completed without errors
- [ ] All Python packages installed successfully
- [ ] Folders created:
  - [ ] audio/
  - [ ] backgrounds/
  - [ ] fonts/
  - [ ] temp/
  - [ ] outputs/

### Step 3: (Optional) Download Fonts
- [ ] Run font download script
  ```powershell
  .\download_fonts.ps1
  ```

- [ ] Fonts downloaded successfully to fonts/ folder
- [ ] At least one .ttf file present in fonts/

---

## 🚀 First Run Checklist

### Step 1: Start Server
- [ ] Open PowerShell in project directory
- [ ] Run main.py
  ```powershell
  python main.py
  ```

- [ ] Server starts without errors
- [ ] Console shows:
  ```
  =====================================================
    Quran Cinematic Reels Generator
  =====================================================
    Server: http://localhost:5000
  =====================================================
  ```

### Step 2: Access Web Interface
- [ ] Open browser
- [ ] Navigate to http://localhost:5000
- [ ] Page loads correctly
- [ ] All form elements visible:
  - [ ] Reciter dropdown
  - [ ] Surah dropdown
  - [ ] Ayah from/to inputs
  - [ ] Generate button

### Step 3: Test Generation
- [ ] Select a reciter (e.g., "عبد الباسط عبد الصمد - مرتل")
- [ ] Select a short surah (e.g., "112. الإخلاص")
- [ ] Enter ayah range: 1 to 1
- [ ] Click "إنشاء الريل الاحترافي"
- [ ] Progress bar appears
- [ ] Status message shows "جاري الإنشاء..."
- [ ] Wait for completion (~30-60 seconds)
- [ ] Success message appears
- [ ] Download button appears
- [ ] Video file can be downloaded
- [ ] Video plays correctly:
  - [ ] Shows moving background
  - [ ] Shows Arabic text
  - [ ] Audio synced with video
  - [ ] Video is vertical (9:16)

---

## 🧪 Testing Checklist

### Basic Tests
- [ ] Single ayah generation works
- [ ] Multiple ayahs generation works (try 2-3)
- [ ] Different reciters work
- [ ] Different surahs work
- [ ] Audio downloads correctly
- [ ] Videos concatenate properly

### Quality Tests
- [ ] Background is smooth and cinematic
- [ ] Text is clear and readable
- [ ] Text has shadow effect
- [ ] Text has glow effect
- [ ] Audio quality is good (192k AAC)
- [ ] Video quality is high (CRF 18)
- [ ] No artifacts or glitches

### Performance Tests
- [ ] Single ayah: ~30-60 seconds
- [ ] 2-3 ayahs: ~1-2 minutes
- [ ] Server responsive during generation
- [ ] Temporary files cleaned up after generation
- [ ] Output files in outputs/ folder

### Error Handling Tests
- [ ] Invalid ayah range shows error
- [ ] Missing fields show error
- [ ] Network issues handled gracefully
- [ ] FFmpeg errors reported clearly

---

## 📦 Files & Folders Checklist

### Core Files (Must Exist)
- [ ] main.py (15.6 KB)
- [ ] index.html (22.5 KB)
- [ ] requirements.txt (0.1 KB)

### Setup Files (Must Exist)
- [ ] setup.ps1 (3.2 KB)
- [ ] download_fonts.ps1 (3.3 KB)
- [ ] test_generator.py (3.1 KB)

### Documentation (Must Exist)
- [ ] README.md (7.8 KB)
- [ ] QUICKSTART.md (4.5 KB)
- [ ] GUIDE.md (13.9 KB)
- [ ] TECHNICAL.md (13.4 KB)
- [ ] EXAMPLES.md (13.4 KB)
- [ ] PROJECT_SUMMARY.md (10+ KB)
- [ ] CHECKLIST.md (this file)

### Folders (Must Exist)
- [ ] audio/ (for cached MP3 files)
- [ ] backgrounds/ (optional custom backgrounds)
- [ ] fonts/ (for Quranic fonts)
- [ ] temp/ (temporary files, auto-cleaned)
- [ ] outputs/ (final videos)

---

## 🔍 Troubleshooting Checklist

### If Server Won't Start
- [ ] Check Python version: `python --version`
- [ ] Check if port 5000 is free
- [ ] Check if all packages installed: `pip list`
- [ ] Try reinstalling requirements: `pip install -r requirements.txt`

### If FFmpeg Errors
- [ ] Check FFmpeg installed: `ffmpeg -version`
- [ ] Check FFmpeg in PATH: `where.exe ffmpeg`
- [ ] Restart PowerShell after adding to PATH
- [ ] Try running a simple FFmpeg command

### If Text Not Rendering
- [ ] Check if fonts/ folder exists
- [ ] Check if any .ttf files in fonts/
- [ ] Run download_fonts.ps1
- [ ] Check Windows font: C:\Windows\Fonts\TRADBDO.TTF

### If Audio Not Downloading
- [ ] Check internet connection
- [ ] Check if everyayah.com is accessible
- [ ] Try different reciter
- [ ] Check audio/ folder permissions

### If Video Quality Poor
- [ ] Check CRF value in main.py (should be 18)
- [ ] Check preset value (should be 'slow')
- [ ] Check resolution (should be 1080x1920)
- [ ] Check if FFmpeg using libx264

---

## 📱 Usage Checklist

### For Instagram Reels
- [ ] Video is 1080x1920 (vertical)
- [ ] Duration under 90 seconds
- [ ] File size reasonable (<50 MB)
- [ ] Audio clear and synced
- [ ] Text readable on mobile
- [ ] Quality suitable for posting

### For TikTok
- [ ] Video is 1080x1920 (vertical)
- [ ] Duration under 60 seconds ideal
- [ ] High quality maintained
- [ ] Audio synced perfectly
- [ ] Text visible and clear

### For YouTube Shorts
- [ ] Video is 1080x1920 (vertical)
- [ ] Duration under 60 seconds
- [ ] Faststart flag enabled
- [ ] High bitrate for quality
- [ ] Thumbnail-worthy first frame

---

## 🎯 Final Verification

### Functionality
- [ ] ✅ Can select reciter
- [ ] ✅ Can select surah
- [ ] ✅ Can select ayah range
- [ ] ✅ Can generate video
- [ ] ✅ Can download video
- [ ] ✅ Video plays correctly

### Quality
- [ ] ✅ Background is cinematic
- [ ] ✅ Text is beautiful
- [ ] ✅ Audio is high quality
- [ ] ✅ Sync is perfect
- [ ] ✅ Resolution is 1080x1920

### Performance
- [ ] ✅ Generation time reasonable
- [ ] ✅ Server stays responsive
- [ ] ✅ Files cleanup properly
- [ ] ✅ No memory leaks

### Documentation
- [ ] ✅ README.md complete
- [ ] ✅ All guides present
- [ ] ✅ Examples clear
- [ ] ✅ Technical docs accurate

---

## 🎉 Success Criteria

### Your setup is successful if:
✅ Server starts without errors  
✅ Web interface loads properly  
✅ Can generate a test video  
✅ Video downloads successfully  
✅ Video plays with correct quality  
✅ All features work as expected  

### If all checkboxes above are checked:
🎊 **Congratulations!**  
🎊 Your Quran Cinematic Reels Generator is fully operational!  
🎊 You can now create beautiful Quran reels!  

---

## 📞 Next Steps After Successful Setup

### 1. Create Your First Real Video
Try creating a meaningful ayah:
- Surah 1 (Al-Fatiha) complete
- Surah 112 (Al-Ikhlas) complete
- Surah 2, Ayah 255 (Ayat Al-Kursi)

### 2. Customize Settings
Read TECHNICAL.md to learn how to:
- Change colors
- Adjust font sizes
- Modify quality settings
- Add custom backgrounds

### 3. Share Your Work
Post your videos on:
- Instagram Reels
- TikTok
- YouTube Shorts
- Facebook Stories

### 4. Contribute
If you find issues or have suggestions:
- Document the issue
- Try to reproduce it
- Share your feedback
- Suggest improvements

---

## 🌙 Final Notes

### Remember:
- Keep Python and FFmpeg updated
- Check documentation for help
- Test before posting to social media
- Share with attribution (optional)
- Make dua for those who benefit

### Optimization Tips:
- Cache audio files (automatically done)
- Use shorter ayahs for faster generation
- Close other heavy applications during generation
- Consider upgrading hardware for better performance

### Best Practices:
- Generate during low-activity times
- Verify video before posting
- Add meaningful captions
- Use relevant hashtags
- Engage with your audience

---

**🎬 Happy Creating! May Allah accept your efforts! 🌙**

---

## 📊 Checklist Summary

**Total Items**: ~150 checkboxes  
**Categories**: 10 sections  
**Estimated Time**: 15-30 minutes for full verification  

**Status Legend**:
- [ ] Not checked / Not done
- [x] Checked / Done
- ✅ Verified and working
- ❌ Failed or needs attention
- ⚠️ Warning or note

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
