# Technical Documentation - Quran Cinematic Reels Generator

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       User Interface                         │
│                      (index.html)                            │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP Request (JSON)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Flask Server (main.py)                    │
├─────────────────────────────────────────────────────────────┤
│  1. API Fetching        │  2. Audio Download                │
│     - Quran text        │     - everyayah.com               │
│     - api.alquran.cloud │     - MP3 format                  │
├─────────────────────────────────────────────────────────────┤
│  3. Background Gen      │  4. Text Overlay                  │
│     - OpenCV + NumPy    │     - PIL + arabic-reshaper       │
│     - Procedural art    │     - Shadow + Glow effects       │
├─────────────────────────────────────────────────────────────┤
│  5. Video Composition                                        │
│     - FFmpeg overlay filter                                  │
│     - Audio sync                                             │
└───────────────────────────┬─────────────────────────────────┘
                            │ Video File (MP4)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Output (9:16 Vertical)                    │
│               1080x1920, CRF 18, AAC 192k                    │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Background Generation (`generate_nature_background`)

**Purpose**: Create cinematic nature-inspired backgrounds procedurally

**Process**:
```python
1. Initialize video writer (OpenCV)
   - Resolution: 1080x1920
   - FPS: 30
   - Codec: mp4v → libx264

2. Choose random color palette
   - Sky blue → Light yellow
   - Turquoise → Peachy
   - Forest green → Light green
   - Light blue → White

3. For each frame (30 * duration):
   a. Generate gradient background
      - Vertical gradient with sine wave distortion
      - Smooth transition between two colors
   
   b. Add floating particles
      - Random position (30 particles/frame)
      - Random size (2-8px)
      - White color with low opacity (10-30%)
      - Simulates dust/light particles
   
   c. Apply Gaussian blur
      - Radius: 15px
      - Applied every 3 frames for performance
   
   d. Write frame to video

4. Re-encode with FFmpeg
   - H.264 codec
   - CRF 23 (high quality)
   - YUV420P pixel format (universal compatibility)
```

**Key Parameters**:
- `width`: 1080px (vertical video width)
- `height`: 1920px (9:16 aspect ratio)
- `duration`: Audio length in seconds
- `fps`: 30 (smooth motion)

**Output**: MP4 video file with smooth nature-inspired animation

---

### 2. Text Overlay Generation (`create_quran_text_overlay`)

**Purpose**: Create beautiful Arabic Quranic text with professional effects

**Process**:
```python
1. Load Quranic Font
   - Priority: TRADBDO.TTF (Traditional Arabic Bold)
   - Fallback: Amiri, Scheherazade, Arial
   - Size: 90px (configurable)

2. Text Reshaping & BiDi
   a. arabic_reshaper.reshape(text)
      - Fixes Arabic letter joining
      - Handles ligatures and forms
   
   b. bidi.algorithm.get_display(reshaped)
      - Right-to-left ordering
      - Proper Arabic text direction

3. Word Wrapping
   - Max width: 960px (1080 - 120px padding)
   - Split by words
   - Measure each line with textbbox
   - Break when exceeds max width

4. Layer 1: Shadow (Dark)
   - Color: Black with 120/255 alpha
   - Offset: 4px in all directions (16 positions)
   - Gaussian blur: radius 3px
   - Creates depth perception

5. Layer 2: Main Text (White)
   - Color: Pure white (255, 255, 255, 255)
   - Positioned at calculated center
   - Sharp and clear

6. Layer 3: Glow (Soft)
   - Color: White with 80/255 alpha
   - Same position as main text
   - Gaussian blur: radius 8px
   - Creates ethereal luminous effect

7. Alpha Compositing
   - Combine all layers: Glow → Shadow → Main
   - Preserve transparency
   - Export as PNG with alpha channel
```

**Key Features**:
- **Multi-layer rendering**: Shadow, main text, glow
- **Arabic text support**: Full reshaping and BiDi
- **Transparent background**: Alpha channel preserved
- **Centered alignment**: Automatic centering
- **Multi-line support**: Automatic word wrapping

**Output**: PNG file with transparent background and layered text

---

### 3. Video Composition (`create_cinematic_video`)

**Purpose**: Combine background, text overlay, and audio into final video

**FFmpeg Command**:
```bash
ffmpeg -y \
  -i background.mp4 \           # Input 1: Nature background
  -i text_overlay.png \         # Input 2: Text (transparent PNG)
  -i audio.mp3 \                # Input 3: Quran recitation
  -filter_complex \
    "[0:v][1:v]overlay=0:0:enable='between(t,0,DURATION)'[v]" \
  -map "[v]" \                  # Use filtered video
  -map "2:a" \                  # Use audio from input 3
  -c:v libx264 \                # H.264 video codec
  -preset slow \                # High quality encoding
  -crf 18 \                     # Very high quality (18/51 scale)
  -c:a aac \                    # AAC audio codec
  -b:a 192k \                   # Audio bitrate
  -pix_fmt yuv420p \            # Universal pixel format
  -t DURATION \                 # Exact duration from audio
  -movflags +faststart \        # Web optimization
  output.mp4
```

**Filter Explanation**:
- `[0:v][1:v]`: Take video from input 0 and 1
- `overlay=0:0`: Position overlay at (0,0) - top-left
- `enable='between(t,0,DURATION)'`: Show overlay during entire video
- `[v]`: Output name for filtered video

**Quality Settings**:
- **CRF 18**: Near-lossless quality (lower = better, 0-51 scale)
- **Preset slow**: Best compression efficiency
- **YUV420P**: Compatible with all devices/players
- **AAC 192k**: High quality audio
- **Faststart**: Enables streaming (metadata at beginning)

---

### 4. Video Concatenation (`concatenate_videos`)

**Purpose**: Join multiple ayah videos into one continuous video

**Process**:
```python
1. Create concat list file:
   file 'video1.mp4'
   file 'video2.mp4'
   file 'video3.mp4'

2. FFmpeg concat demuxer:
   ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

3. Clean up temporary files
```

**Note**: Uses `-c copy` for fast concatenation without re-encoding

---

## Data Flow

### Complete Request Flow:

```
User clicks "Generate" →
│
├─→ For each ayah:
│   │
│   ├─→ Fetch text from api.alquran.cloud
│   │   GET http://api.alquran.cloud/v1/ayah/{surah}:{ayah}
│   │   Response: {"data": {"text": "...", ...}}
│   │
│   ├─→ Download audio from everyayah.com
│   │   GET https://everyayah.com/data/{reciter}/{surah:03d}{ayah:03d}.mp3
│   │   Save to: audio/{reciter}_{surah}_{ayah}.mp3
│   │
│   ├─→ Generate background video
│   │   OpenCV → temp/bg_nature_{timestamp}.mp4
│   │   Duration: from audio file (pydub)
│   │
│   ├─→ Create text overlay
│   │   PIL → temp/text_overlay_{timestamp}.png
│   │   Multi-layer: shadow + text + glow
│   │
│   ├─→ Compose final video
│   │   FFmpeg overlay → temp/video_{surah}_{ayah}_{timestamp}.mp4
│   │
│   └─→ Clean temporary files
│       Delete: bg_nature_*.mp4, text_overlay_*.png
│
└─→ Concatenate all videos
    FFmpeg concat → outputs/quran_reel_{surah}_{from}-{to}_{timestamp}.mp4
    Return URL to frontend
```

---

## File Structure

```
Quran/
│
├── main.py                    # Core application
│   ├── Flask routes
│   ├── Video generation logic
│   ├── Background generation
│   └── Text processing
│
├── index.html                 # Web interface
│   ├── Surah/Ayah selection
│   ├── Progress tracking
│   └── Download button
│
├── requirements.txt           # Python dependencies
│
├── setup.ps1                  # Auto-setup script
├── download_fonts.ps1         # Font downloader
│
├── audio/                     # Downloaded MP3 files (cached)
├── backgrounds/               # Optional custom backgrounds
├── fonts/                     # Quranic fonts
├── temp/                      # Temporary files (auto-cleaned)
└── outputs/                   # Final videos
```

---

## Performance Optimization

### Current Implementation:
- **Caching**: Audio files cached after first download
- **Parallel Processing**: Could be added for multiple ayahs
- **GPU Acceleration**: Not used (pure CPU)
- **Temporary File Cleanup**: Automatic after each ayah

### Potential Improvements:
1. **Use GPU**: OpenCV with CUDA for faster rendering
2. **Parallel Generation**: Process multiple ayahs simultaneously
3. **Background Templates**: Pre-generate backgrounds at different durations
4. **Font Caching**: Keep font objects in memory
5. **FFmpeg Hardware Encoding**: Use `-hwaccel` flags

---

## Configuration Options

### Video Quality:
```python
# In create_cinematic_video():
'-crf', '18'          # Range: 0-51 (lower = better)
'-preset', 'slow'     # Options: ultrafast, fast, medium, slow, veryslow
'-b:a', '192k'        # Audio bitrate
```

### Text Appearance:
```python
# In create_quran_text_overlay():
font_size = 90                        # Text size
shadow_offset = 4                     # Shadow distance
shadow_color = (0, 0, 0, 120)        # Shadow color + alpha
glow_radius = 8                       # Glow blur radius
```

### Background Colors:
```python
# In generate_nature_background():
base_colors = [
    [(R1, G1, B1), (R2, G2, B2)],    # Gradient start → end
    # Add more color schemes
]
```

---

## Troubleshooting

### Issue: "FFmpeg not found"
**Solution**: Install FFmpeg and add to PATH
```powershell
# Check if FFmpeg is accessible:
ffmpeg -version
```

### Issue: "Font rendering poor quality"
**Solution**: Download Quranic fonts
```powershell
.\download_fonts.ps1
```

### Issue: "Video generation too slow"
**Solution**: Reduce quality settings
```python
'-crf', '23'          # Instead of 18
'-preset', 'medium'   # Instead of slow
fps = 24              # Instead of 30
```

### Issue: "Text too small/large"
**Solution**: Adjust font size
```python
font_size = 70   # Smaller
font_size = 110  # Larger
```

---

## API Endpoints

### POST `/generate`
Generate Quran video reel

**Request**:
```json
{
  "reciter": "abdulbasit/murattal",
  "surah": 1,
  "ayah_from": 1,
  "ayah_to": 3
}
```

**Response** (Success):
```json
{
  "success": true,
  "video_url": "/outputs/quran_reel_1_1-3_20260201_123456.mp4",
  "message": "Cinematic Quran Reel created successfully!"
}
```

**Response** (Error):
```json
{
  "error": "Failed to download audio for ayah 2"
}
```

### GET `/outputs/<filename>`
Download generated video

**Response**: MP4 video file

---

## External Dependencies

### APIs:
- **api.alquran.cloud**: Quran text (Arabic)
  - Endpoint: `/v1/ayah/{surah}:{ayah}`
  - Format: JSON
  - Free, no auth required

- **everyayah.com**: Quran audio recitations
  - Endpoint: `/data/{reciter}/{surah:03d}{ayah:03d}.mp3`
  - Format: MP3
  - Free, no auth required

### Software:
- **FFmpeg**: Video processing
  - Version: 4.0+
  - Required features: libx264, aac

- **Python**: 3.8+
  - Required for all libraries

---

## License & Credits

**Made with ❤️ for Quran**

This project is free to use for personal and educational purposes.

**Data Sources**:
- Quran text: api.alquran.cloud
- Recitations: everyayah.com

**Technologies**:
- Flask (Web framework)
- OpenCV (Video generation)
- PIL/Pillow (Image processing)
- FFmpeg (Video composition)
- arabic-reshaper (Arabic text)
- python-bidi (BiDi algorithm)
