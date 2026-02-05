# Examples & Use Cases

## Quick Examples

### Example 1: Single Ayah (Al-Fatiha, Verse 1)
```json
Request:
{
  "reciter": "abdulbasit/murattal",
  "surah": 1,
  "ayah_from": 1,
  "ayah_to": 1
}

Result:
- Duration: ~5 seconds
- Size: ~1-2 MB
- Processing time: ~30-45 seconds
```

### Example 2: Short Surah (Al-Ikhlas)
```json
Request:
{
  "reciter": "sudais",
  "surah": 112,
  "ayah_from": 1,
  "ayah_to": 4
}

Result:
- Duration: ~15-20 seconds
- Size: ~3-5 MB
- Processing time: ~2-3 minutes
- Perfect for Instagram Reels
```

### Example 3: Famous Ayah (Ayat Al-Kursi)
```json
Request:
{
  "reciter": "minshawi/mujawwad",
  "surah": 2,
  "ayah": 255,
  "ayah_to": 255
}

Result:
- Duration: ~2-3 minutes
- Size: ~15-20 MB
- Processing time: ~2-3 minutes
- Cinematic quality
```

---

## Visual Comparison

### Traditional vs. This Generator

```
┌─────────────────────────────────────────────────────────────┐
│                    Traditional Method                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Find background video (stock footage)                    │
│ 2. Download Quran audio separately                          │
│ 3. Open After Effects / Premiere Pro                        │
│ 4. Import assets                                            │
│ 5. Manually position text                                   │
│ 6. Add effects (shadow, glow)                               │
│ 7. Sync audio                                               │
│ 8. Render (10-30 minutes)                                   │
│ 9. Export                                                    │
│                                                              │
│ Total Time: 30-60 minutes per video                         │
│ Requires: Paid software, video editing skills               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    This Generator                            │
├─────────────────────────────────────────────────────────────┤
│ 1. Open web interface                                       │
│ 2. Select reciter, surah, ayah range                        │
│ 3. Click "Generate"                                         │
│ 4. Wait 30-60 seconds                                       │
│ 5. Download                                                  │
│                                                              │
│ Total Time: 1-3 minutes                                     │
│ Requires: Nothing (fully automatic)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Visual Effects Breakdown

### Text Rendering Pipeline

```
Step 1: Base Text (White)
┌─────────────────────────┐
│                         │
│   بِسْمِ اللَّهِ        │
│                         │
└─────────────────────────┘

Step 2: Add Shadow (Black, Blurred)
┌─────────────────────────┐
│    ░░░░░░░░░░░░         │
│   بِسْمِ اللَّهِ        │
│    ░░░░░░░░░░░░         │
└─────────────────────────┘

Step 3: Add Glow (White, Very Blurred)
┌─────────────────────────┐
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         │
│   بِسْمِ اللَّهِ        │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         │
└─────────────────────────┘

Final Result: Layered Composition
┌─────────────────────────┐
│  ╔════════════════╗     │
│  ║ بِسْمِ اللَّهِ ║     │
│  ╚════════════════╝     │
│                         │
│ - Crisp white text      │
│ - Soft dark shadow      │
│ - Ethereal glow         │
│ - Professional look     │
└─────────────────────────┘
```

---

## Background Animation Frames

```
Frame 1 (0.0s):
┌─────────────────┐
│ ░░░░░░░░░░░░░░  │  Sky blue top
│ ░░░░░▓▓░░░░░░░  │  Gradient transition
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  Light yellow bottom
│ ▓▓▓▓▓░▓▓▓▓▓▓▓▓  │  + Floating particles
└─────────────────┘

Frame 15 (0.5s):
┌─────────────────┐
│ ░░░░░░░░░░░░░░  │  Slight color shift
│ ░░▓▓░░░░░░▓░░░  │  Particles moved
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  Wave distortion
│ ▓▓▓▓▓▓▓▓░▓▓▓▓▓  │  Smooth transition
└─────────────────┘

Frame 30 (1.0s):
┌─────────────────┐
│ ░░░░░░░░░░░░░░  │  Continuous flow
│ ░░░░░░▓░░░░░░░  │  New particles
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  Gradient animation
│ ▓▓░▓▓▓▓▓▓▓▓▓▓▓  │  Natural movement
└─────────────────┘
```

---

## Color Palettes Used

### Palette 1: Sky & Sun
```
Top:    #87CEEB (Sky Blue)
Bottom: #FFFDD0 (Light Yellow)

Use case: Daytime, peaceful scenes
Mood: Calm, hopeful, bright
```

### Palette 2: Ocean & Sand
```
Top:    #B0E0E6 (Powder Blue)
Bottom: #FFE4C4 (Bisque)

Use case: Beach, serene nature
Mood: Tranquil, warm, soothing
```

### Palette 3: Forest & Light
```
Top:    #93C572 (Forest Green)
Bottom: #B8E994 (Light Green)

Use case: Nature, gardens
Mood: Fresh, natural, life
```

### Palette 4: Dawn Sky
```
Top:    #ADD8E6 (Light Blue)
Bottom: #F0F8FF (Alice Blue)

Use case: Early morning, spiritual
Mood: Pure, clean, divine
```

---

## Video Specifications

### Resolution & Aspect Ratio
```
┌──────────────┐
│              │ ← 1080px wide
│              │
│              │
│   9:16       │
│   Vertical   │
│              │
│              │
│              │
│              │
└──────────────┘
      ↑
   1920px tall

Perfect for:
✓ Instagram Reels (1080x1920)
✓ TikTok (1080x1920)
✓ YouTube Shorts (1080x1920)
✓ Facebook Stories (1080x1920)
```

### Encoding Details
```
Video:
- Codec: H.264 (AVC)
- Profile: High
- Level: 4.0
- Pixel Format: YUV420P
- Bitrate: Variable (CRF 18)
- Frame Rate: 30 fps

Audio:
- Codec: AAC-LC
- Sample Rate: 48000 Hz
- Channels: Stereo
- Bitrate: 192 kbps

Container:
- Format: MP4
- Flags: +faststart (streaming optimized)
```

---

## Use Case Scenarios

### 1. Daily Quran Content Creator
**Goal**: Post one ayah per day on social media

**Workflow**:
```
Monday:    Surah Al-Baqarah, Ayah 1
Tuesday:   Surah Al-Baqarah, Ayah 2
Wednesday: Surah Al-Baqarah, Ayah 3
...

Time saved: 25 minutes per video
Monthly output: 30 videos in 30 minutes total
```

### 2. Ramadan Special Series
**Goal**: Create 30-day Ramadan video series

**Example**:
```
Day 1:  Al-Fatiha (Complete)
Day 2:  Ayat Al-Kursi
Day 3:  Last 2 verses of Al-Baqarah
...
Day 30: Al-Nas (Complete)

Batch generation: 30 videos in 1 hour
```

### 3. Memorization Helper
**Goal**: Create videos for students to memorize

**Features**:
- Clear text display
- Synchronized audio
- Repeat-friendly format
- Beautiful visuals aid memory

### 4. Reminder/Motivation Posts
**Goal**: Share inspirational verses

**Examples**:
- Patience verses (Surah Al-Baqarah, 153)
- Gratitude verses (Surah Ibrahim, 7)
- Strength verses (Surah Al-Inshirah, 5-6)

---

## Platform-Specific Tips

### Instagram Reels
```
✓ Perfect 9:16 ratio
✓ Under 90 seconds ideal
✓ Engaging first 3 seconds
✓ Add hashtags in caption
✓ Post during peak hours

Recommendation: 1-3 ayahs per reel
```

### TikTok
```
✓ 9:16 vertical format
✓ 15-60 seconds optimal
✓ Hook viewers immediately
✓ Use trending sounds (audio)
✓ Add text captions

Recommendation: Single short ayah
```

### YouTube Shorts
```
✓ 9:16 vertical required
✓ Under 60 seconds
✓ Eye-catching thumbnail
✓ Clear title
✓ SEO-optimized description

Recommendation: Famous verses
```

### Facebook Stories
```
✓ 9:16 vertical
✓ 15 seconds ideal
✓ Mobile-first design
✓ Clear call-to-action
✓ Share to groups

Recommendation: Short motivational ayahs
```

---

## Advanced Customization Examples

### Custom Font Installation
```powershell
# Download Amiri font
Invoke-WebRequest -Uri "https://github.com/aliftype/amiri/releases/latest" -OutFile "amiri.zip"

# Extract to fonts folder
Expand-Archive amiri.zip -DestinationPath .\fonts\

# Generator will auto-detect
```

### Batch Processing Script
```python
# Generate multiple videos automatically
ayah_ranges = [
    (1, 1, 7),      # Al-Fatiha
    (112, 1, 4),    # Al-Ikhlas
    (113, 1, 5),    # Al-Falaq
    (114, 1, 6),    # An-Nas
]

for surah, start, end in ayah_ranges:
    # Make API request
    # Wait for completion
    # Download result
```

---

## Quality Comparison

### CRF Values Explained
```
CRF 0:  Lossless (HUGE files, 100+ MB/min)
CRF 18: Near-lossless (5-10 MB/min) ← DEFAULT
CRF 23: High quality (2-5 MB/min)
CRF 28: Medium quality (1-2 MB/min)
CRF 35: Low quality (500 KB-1 MB/min)
CRF 51: Worst quality (tiny files)

Recommendation: Keep at 18 for best results
```

### Preset Speed vs Quality
```
ultrafast: 30 sec encoding, 200% file size
superfast: 45 sec encoding, 150% file size
veryfast:  60 sec encoding, 120% file size
faster:    75 sec encoding, 110% file size
fast:      90 sec encoding, 105% file size
medium:    120 sec encoding, 100% file size
slow:      180 sec encoding, 95% file size  ← DEFAULT
slower:    240 sec encoding, 92% file size
veryslow:  360 sec encoding, 90% file size

Recommendation: 'slow' balances quality and speed
```

---

## Troubleshooting Common Issues

### Issue: Text is cut off
```
Solution: Reduce font size

# In main.py:
create_quran_text_overlay(text, width=1080, height=1920, font_size=70)
                                                            # ↑ from 90
```

### Issue: Background too bright
```
Solution: Choose darker color palette

# In main.py, generate_nature_background():
base_colors = [
    [(60, 80, 100), (120, 140, 160)],   # Darker blues
]
```

### Issue: Video stutters
```
Solution: Reduce FPS or use faster preset

# In main.py:
fps = 24  # Instead of 30
'-preset', 'fast'  # Instead of 'slow'
```

### Issue: Audio out of sync
```
Cause: Usually FFmpeg version issue
Solution: Update FFmpeg to latest version
```

---

## Performance Benchmarks

### Test System: Intel i5, 8GB RAM, No GPU

| Ayahs | Duration | Processing Time | File Size |
|-------|----------|----------------|-----------|
| 1     | 5s       | 35s            | 1.5 MB    |
| 2     | 12s      | 65s            | 3 MB      |
| 3     | 20s      | 95s            | 5 MB      |
| 5     | 35s      | 160s           | 8 MB      |
| 7     | 50s      | 230s           | 12 MB     |

**Note**: Processing time includes:
- Background generation (50%)
- Text rendering (20%)
- FFmpeg encoding (30%)

---

## Future Enhancement Ideas

### Planned Features:
- [ ] Multiple background styles (forest, ocean, mountains)
- [ ] Text animation (fade in, word-by-word)
- [ ] Translation overlay (English, Urdu, etc.)
- [ ] Custom color schemes
- [ ] Background music (nasheed)
- [ ] Verse-by-verse highlighting
- [ ] Progress bar indicator
- [ ] Batch generation interface

### Community Requests:
- [ ] Landscape format (16:9)
- [ ] Square format (1:1)
- [ ] Multiple reciter audio (comparison)
- [ ] Tafsir text overlay
- [ ] Surah intro cards
- [ ] End screen with channel info

---

**Created with ❤️ for the Quran Community**

For more examples and inspiration, visit popular Islamic content creators on:
- Instagram: @qurandaily, @islamicreminders
- TikTok: #quranreels #islamicshorts
- YouTube: Quran Shorts channels
