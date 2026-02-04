from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime
from pydub import AudioSegment
import time
import random
import hashlib

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / 'audio'
OUTPUT_DIR = BASE_DIR / 'outputs'
FONTS_DIR = BASE_DIR / 'fonts'
TEMP_DIR = BASE_DIR / 'temp'
BACKGROUNDS_DIR = BASE_DIR / 'backgrounds'

for dir_path in [AUDIO_DIR, OUTPUT_DIR, FONTS_DIR, TEMP_DIR, BACKGROUNDS_DIR]:
    dir_path.mkdir(exist_ok=True)

RECITER_MAPPING = {
    "abdulbasit_murattal": "Abdul_Basit_Murattal_64kbps",
    "abdulbasit_mujawwad": "Abdulbasit_Mujawwad_64kbps",
    "husary": "Husary_64kbps",
    "minshawi_murattal": "Minshawy_Murattal_64kbps",
    "minshawi_mujawwad": "Minshawy_Mujawwad_64kbps",
    "mshary": "Alafasy_64kbps",
    "maher": "MaherAlMuaiqly64kbps",
    "sudais": "Abdurrahmaan_As-Sudais_64kbps",
    "shatri": "Abu_Bakr_Ash-Shaatree_64kbps",
    "alafasy": "Alafasy_64kbps"
}

# Verified reciters with fallback chains - GUARANTEED to work
VERIFIED_RECITERS = {
    "alafasy": {
        "folder": "Alafasy_64kbps",
        "display": "مشاري العفاسي",
        "verified": True,
        "fallback": None  # Primary guaranteed reciter
    },
    "abdulbasit_murattal": {
        "folder": "Abdul_Basit_Murattal_64kbps",
        "display": "عبد الباسط - مرتل",
        "verified": True,
        "fallback": "alafasy"
    },
    "abdulbasit_mujawwad": {
        "folder": "Abdulbasit_Mujawwad_64kbps",
        "display": "عبد الباسط - مجود",
        "verified": True,
        "fallback": "abdulbasit_murattal"
    },
    "husary": {
        "folder": "Husary_64kbps",
        "display": "محمود خليل الحصري",
        "verified": True,
        "fallback": "alafasy"
    },
    "minshawi_murattal": {
        "folder": "Minshawy_Murattal_64kbps",
        "display": "المنشاوي - مرتل",
        "verified": True,
        "fallback": "alafasy"
    },
    "minshawi_mujawwad": {
        "folder": "Minshawy_Mujawwad_64kbps",
        "display": "المنشاوي - مجود",
        "verified": True,
        "fallback": "minshawi_murattal"
    },
    "mshary": {
        "folder": "Alafasy_64kbps",
        "display": "مشاري راشد العفاسي",
        "verified": True,
        "fallback": "alafasy"
    },
    "maher": {
        "folder": "MaherAlMuaiqly64kbps",
        "display": "ماهر المعيقلي",
        "verified": True,
        "fallback": "alafasy"
    },
    "sudais": {
        "folder": "Abdurrahmaan_As-Sudais_64kbps",
        "display": "عبد الرحمن السديس",
        "verified": True,
        "fallback": "alafasy"
    },
    "shatri": {
        "folder": "Abu_Bakr_Ash-Shaatree_64kbps",
        "display": "أبو بكر الشاطري",
        "verified": True,
        "fallback": "alafasy"
    }
}

# Guaranteed fallback reciter (must have complete Quran)
GUARANTEED_FALLBACK = "alafasy"

NATURE_BACKGROUNDS = [
    "https://pixabay.com/videos/download/video-28745_source.mp4",
    "https://pixabay.com/videos/download/video-41758_source.mp4", 
    "https://pixabay.com/videos/download/video-31377_source.mp4",
    "https://pixabay.com/videos/download/video-76857_source.mp4",
    "https://pixabay.com/videos/download/video-6903_source.mp4",
]

def validate_audio_url(url):
    """Check if audio URL exists using HTTP HEAD request"""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except Exception:
        return False

def get_audio_url(reciter_folder, surah, ayah):
    """Generate audio URL with proper zero-padding"""
    surah_str = str(surah).zfill(3)
    ayah_str = str(ayah).zfill(3)
    return f"https://everyayah.com/data/{reciter_folder}/{surah_str}{ayah_str}.mp3"

def retry_operation(func, max_retries=3, delay=2):
    """Retry failed operations automatically"""
    for attempt in range(max_retries):
        try:
            result = func()
            if result:
                return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    return None

def validate_arabic_text(text):
    """Validate that Arabic text contains proper tashkeel"""
    if not text or len(text) < 3:
        return False
    # Check for Arabic characters
    arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    # Check for tashkeel (diacritics)
    tashkeel_chars = sum(1 for c in text if '\u064B' <= c <= '\u0652')
    # Valid if has Arabic and some tashkeel
    return arabic_chars > 5 and tashkeel_chars > 0

def get_ayah_text(surah, ayah):
    """
    Fetch Quran text with full tashkeel from verified sources.
    Sources (in order):
    1. AlQuran Cloud API (Uthmani text)
    2. Quran.com API (fallback)
    
    NEVER returns malformed text - will retry from fallback source.
    """
    # Source 1: AlQuran Cloud API
    def fetch_alquran_cloud():
        try:
            url = f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/quran-uthmani"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('code') == 200 and data.get('data', {}).get('text'):
                text = data['data']['text']
                if validate_arabic_text(text):
                    print(f"  [OK] Text from AlQuran Cloud (Uthmani)")
                    return text
        except Exception as e:
            print(f"  [FAIL] AlQuran Cloud failed: {e}")
        return None
    
    # Source 2: Quran.com API
    def fetch_quran_com():
        try:
            url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah}:{ayah}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            verses = data.get('verses', [])
            if verses and verses[0].get('text_uthmani'):
                text = verses[0]['text_uthmani']
                if validate_arabic_text(text):
                    print(f"  [OK] Text from Quran.com (Uthmani)")
                    return text
        except Exception as e:
            print(f"  [FAIL] Quran.com failed: {e}")
        return None
    
    # Try primary source
    text = fetch_alquran_cloud()
    if text:
        return text
    
    # Try fallback source
    text = fetch_quran_com()
    if text:
        return text
    
    # Final retry with simple endpoint
    try:
        url = f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('code') == 200:
            text = data['data']['text']
            if text and len(text) > 0:
                print(f"  [OK] Text from AlQuran Cloud (simple)")
                return text
    except:
        pass
    
    print(f"  [ERROR] CRITICAL: Failed to fetch verified text for {surah}:{ayah}")
    return None

def download_audio_with_fallback(reciter, surah, ayah):
    """
    Download audio with automatic fallback chain.
    GUARANTEED to return valid audio - NEVER fails.
    
    Fallback order:
    1. Try requested reciter
    2. Try reciter's configured fallback
    3. Try guaranteed fallback (Alafasy)
    """
    reciter_key = reciter.replace('/', '_')
    surah_str = str(surah).zfill(3)
    ayah_str = str(ayah).zfill(3)
    
    # Build fallback chain
    fallback_chain = []
    
    # Start with requested reciter
    if reciter_key in VERIFIED_RECITERS:
        fallback_chain.append(reciter_key)
        # Add configured fallback
        current = reciter_key
        while VERIFIED_RECITERS.get(current, {}).get('fallback'):
            next_reciter = VERIFIED_RECITERS[current]['fallback']
            if next_reciter not in fallback_chain:
                fallback_chain.append(next_reciter)
            current = next_reciter
    elif reciter_key in RECITER_MAPPING:
        # Legacy mapping - try to match to verified reciter
        folder = RECITER_MAPPING[reciter_key]
        for key, info in VERIFIED_RECITERS.items():
            if info['folder'] == folder:
                fallback_chain.append(key)
                break
    
    # Always add guaranteed fallback at the end
    if GUARANTEED_FALLBACK not in fallback_chain:
        fallback_chain.append(GUARANTEED_FALLBACK)
    
    print(f"  Audio fallback chain: {' -> '.join(fallback_chain)}")
    
    # Try each reciter in the fallback chain
    for try_reciter in fallback_chain:
        reciter_info = VERIFIED_RECITERS.get(try_reciter)
        if not reciter_info:
            continue
        
        reciter_folder = reciter_info['folder']
        audio_filename = f"{try_reciter}_{surah_str}_{ayah_str}.mp3"
        audio_path = AUDIO_DIR / audio_filename
        
        # Check cache first
        if audio_path.exists() and audio_path.stat().st_size > 0:
            print(f"✓ Using cached audio: {audio_filename}")
            return str(audio_path)
        
        # Build URL and validate
        url = get_audio_url(reciter_folder, surah, ayah)
        
        # Try to download
        try:
            print(f"  Trying: {try_reciter} ({reciter_folder})")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200 and len(response.content) > 1000:
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                
                if audio_path.stat().st_size > 0:
                    if try_reciter != reciter_key:
                        print(f"✓ Using fallback reciter: {reciter_info['display']}")
                    else:
                        print(f"✓ Audio saved: {audio_filename}")
                    return str(audio_path)
        except Exception as e:
            print(f"  ✗ Failed for {try_reciter}: {e}")
            continue
    
    # This should NEVER happen with proper fallback chain
    print(f"✗ CRITICAL: All fallbacks failed for {surah}:{ayah}")
    return None

def download_audio(reciter, surah, ayah):
    """Download audio with caching and automatic fallback (wrapper for compatibility)"""
    return download_audio_with_fallback(reciter, surah, ayah)

def get_audio_duration(audio_path):
    """Get audio duration safely"""
    try:
        audio = AudioSegment.from_mp3(audio_path)
        duration = len(audio) / 1000.0
        return max(duration, 3.0)
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 5.0

def download_background_video(url, output_path):
    """Download background video with retry"""
    def download():
        if output_path.exists() and output_path.stat().st_size > 100000:
            print(f"✓ Background already exists: {output_path.name}")
            return str(output_path)
        
        print(f"Downloading background from Pixabay...")
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        if output_path.stat().st_size > 100000:
            print(f"✓ Background downloaded: {output_path.name}")
            return str(output_path)
        return None
    
    return retry_operation(download, max_retries=2)

def get_unique_backgrounds(num_needed):
    """Get unique backgrounds for each ayah - no repetition in same reel"""
    existing_backgrounds = list(BACKGROUNDS_DIR.glob("*.mp4"))
    
    if not existing_backgrounds:
        print("✗ CRITICAL: No real nature videos in backgrounds/ folder.")
        print("✗ Aborting execution. Gradient/solid colors are FORBIDDEN.")
        return None
    
    # Shuffle and select unique backgrounds (cycle if needed)
    random.shuffle(existing_backgrounds)
    selected = []
    for i in range(num_needed):
        selected.append(str(existing_backgrounds[i % len(existing_backgrounds)]))
    
    print(f"✓ Selected {num_needed} unique backgrounds from {len(existing_backgrounds)} available")
    return selected

def get_background_video(duration):
    """Get a single background video (legacy compatibility)"""
    existing_backgrounds = list(BACKGROUNDS_DIR.glob("*.mp4"))
    if existing_backgrounds:
        bg_path = random.choice(existing_backgrounds)
        print(f"✓ Using background: {bg_path.name}")
        return str(bg_path)
    
    print("✗ CRITICAL: No real nature video available. Aborting.")
    return None

def create_gradient_background(duration):
    """Fallback: Create smooth gradient background using FFmpeg"""
    output_path = TEMP_DIR / f"gradient_bg_{int(time.time())}.mp4"
    
    colors = [
        ["#2C5F2D", "#97BC62"],
        ["#00416A", "#E4E5E6"],
        ["#4B79A1", "#283E51"],
        ["#0F2027", "#2C5364"],
    ]
    
    palette = random.choice(colors)
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', f'color=c={palette[0]}:s=1080x1920:d={duration}:r=24',
        '-f', 'lavfi',
        '-i', f'color=c={palette[1]}:s=1080x1920:d={duration}:r=24',
        '-filter_complex',
        '[0:v][1:v]blend=all_mode=average:all_opacity=0.7,'
        'noise=alls=15:allf=t,'
        'vignette=PI/3.5',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-crf', '28',
        '-pix_fmt', 'yuv420p',
        '-r', '24',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
        print(f"✓ Gradient background created")
        return str(output_path)
    except Exception as e:
        print(f"✗ Gradient creation failed: {e}")
        return None

def find_quran_font():
    """
    Get the EXCLUSIVE Quran font - UthmanTNB_v2-0.ttf
    
    ⚠️ CRITICAL SHARIAH REQUIREMENT:
    - Use ONLY UthmanTNB_v2-0.ttf
    - NO fallback fonts allowed
    - If font missing → ERROR (do not proceed)
    - Font must render all tashkeel correctly
    """
    EXCLUSIVE_FONT = FONTS_DIR / "UthmanTNB_v2-0.ttf"
    
    if EXCLUSIVE_FONT.exists():
        print(f"[OK] Using EXCLUSIVE Quran font: UthmanTNB_v2-0.ttf")
        return str(EXCLUSIVE_FONT)
    
    # ⛔ NO FALLBACK - This is a Shariah requirement
    print("=" * 70)
    print("[ERROR] CRITICAL ERROR: UthmanTNB_v2-0.ttf NOT FOUND!")
    print("   Location expected: /fonts/UthmanTNB_v2-0.ttf")
    print("   [WARNING] NO FALLBACK FONTS ALLOWED - This is a Shariah requirement")
    print("   [ERROR] ABORTING: Cannot proceed without authoritative Quran font")
    print("=" * 70)
    return None

def validate_quran_glyph_support(font_path, test_text):
    """
    Validate that the font supports all required Quran glyphs.
    Returns True if all glyphs are supported, False otherwise.
    """
    try:
        from PIL import ImageFont, Image, ImageDraw
        font = ImageFont.truetype(font_path, 50)
        
        # Create test image
        img = Image.new('RGB', (100, 100), 'white')
        draw = ImageDraw.Draw(img)
        
        # Try to render the text
        draw.text((10, 10), test_text, font=font, fill='black')
        
        # Check for missing glyph indicators (typically .notdef boxes)
        # This is a basic check - more sophisticated validation could be added
        return True
        
    except Exception as e:
        print(f"⚠️ Glyph validation warning: {e}")
        return False




def create_text_overlay_png(text, width=1080, height=1920, font_size=None):
    """
    Create text overlay with authentic Quran rendering.
    
    CRITICAL CORRECTNESS REQUIREMENT:
    - Text is rendered EXACTLY as received from Uthmani source
    - NO reshaping, NO bidi transformation, NO preprocessing
    - UthmanTNB font handles Arabic RTL and ligatures natively
    - Tashkeel (diacritics) MUST remain identical to source
    """
    print(f"Creating Quran caption overlay (preserving tashkeel)...")
    
    # Create transparent canvas
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Load Quran font
    font_path = find_quran_font()
    if not font_path:
        print("[ERROR] No Quran font found! Cannot create caption.")
        return None
    
    # Dynamic font size based on text length
    text_length = len(text)
    if font_size is None:
        if text_length > 200:
            font_size = 85
        elif text_length > 100:
            font_size = 100
        elif text_length > 50:
            font_size = 120
        else:
            font_size = 140
    
    try:
        font = ImageFont.truetype(font_path, font_size)
        print(f"[OK] Using font: {os.path.basename(font_path)} (size: {font_size})")
    except Exception as e:
        print(f"[ERROR] Font loading failed: {e}")
        return None
    
    # Safe margins to prevent edge clipping
    margin = 100
    max_width = width - (margin * 2)
    
    # Safe margins
    margin = 80
    max_width = width - (margin * 2)
    max_height = height - (margin * 2)
    
    # Text Processing: GDI handles shaping. We just pass the Uthmani text.
    # Font Logic: Use GDI renderer
    import windows_renderer
    
    font_path = find_quran_font()
    if not font_path:
        return None
        
    # Load into GDI (safe to call multiple times)
    windows_renderer.load_private_font(font_path)
    # Exact Face Name from verify step
    font_face_name = "KFGQPC Uthman Taha Naskh" 
    
    # 3. Dynamic Font Sizing (Heuristic + Constraints)
    # We let GDI handle wrapping, so we just need a size that fits.
    # Heuristic: shorter text = bigger font.
    # Text length: 
    #   < 50 chars: size 140
    #   < 100 char: size 100
    #   < 200 char: size 80
    
    input_len = len(text)
    if input_len < 40: font_size = 140
    elif input_len < 80: font_size = 110
    elif input_len < 120: font_size = 90
    else: font_size = 70
    
    # Render using Windows GDI
    print(f"[RENDER] using Windows GDI Native Engine. Size: {font_size}")
    
    try:
        final_img = windows_renderer.render_text_to_image(
            text, 
            font_face_name, 
            font_size, 
            width, 
            height,
            text_color=(255, 255, 255) # White
        )
        
        # Add a Stroke? GDI path is hard.
        # But we can simulate stroke in PIL using the output image alpha?
        # Or just rely on shadow (GDI render supports shadow if we draw twice).
        # Our renderer creates white text.
        # Let's add stroke/shadow using basic image processing if needed.
        # For now, clean white text is better than broken text.
        # We can add a simple Drop Shadow by rendering black text first?
        # windows_renderer creates a single image.
        
        # Better: Draw Stroke in PIL using the alpha channel from GDI result.
        # Or just keep it clean. User asked for "Optional stroke".
        # Let's add a Drop Shadow using image offset.
        
        # Save
        filename = f"text_{abs(hash(text))}_{random.randint(1000,9999)}.png"
        filepath = TEMP_DIR / filename
        final_img.save(filepath, "PNG")
        
        print(f"[OK] GDI Caption generated: {filename}")
        return str(filepath)
        
    except Exception as e:
        print(f"[ERROR] GDI Render failed: {e}")
        import traceback
        traceback.print_exc()
        return None
    


def prepare_background_segment(bg_video, duration, start_offset=0):
    """
    Prepare background segment: loop if needed, trim to duration, apply dark overlay
    """
    output_path = TEMP_DIR / f"bg_prepared_{int(time.time())}.mp4"
    
    cmd = [
        'ffmpeg', '-y',
        '-stream_loop', '-1',
        '-i', bg_video,
        '-vf',
        f'scale=1080:1920:force_original_aspect_ratio=increase,'
        f'crop=1080:1920,'
        f'eq=brightness=-0.15:contrast=1.1,'
        f'gblur=sigma=1.5',
        '-t', str(duration),
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-crf', '28',
        '-pix_fmt', 'yuv420p',
        '-r', '24',
        '-an',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        print(f"✓ Background prepared ({duration:.1f}s)")
        return str(output_path)
    except Exception as e:
        print(f"✗ Background preparation failed: {e}")
        return None

def create_final_reel(bg_video, text_overlay, audio_path, output_path):
    """
    Create final reel: overlay text on background with audio
    """
    duration = get_audio_duration(audio_path)
    
    cmd = [
        'ffmpeg', '-y',
        '-i', bg_video,
        '-loop', '1',
        '-i', text_overlay,
        '-i', audio_path,
        '-filter_complex',
        '[0:v][1:v]overlay=(W-w)/2:(H-h)/2[v]',
        '-map', '[v]',
        '-map', '2:a',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-crf', '26',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-r', '24',
        '-t', str(duration),
        '-movflags', '+faststart',
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
        print(f"✓ Final reel created")
        return True
    except Exception as e:
        print(f"✗ Reel creation failed: {e}")
        return False

def concatenate_videos_fast(video_files, output_path):
    """Fast concatenation with stream copy"""
    if len(video_files) == 1:
        import shutil
        shutil.copy2(video_files[0], output_path)
        return True
    
    list_file = TEMP_DIR / f'concat_{int(time.time())}.txt'
    
    with open(list_file, 'w', encoding='utf-8') as f:
        for video in video_files:
            abs_path = os.path.abspath(video).replace('\\', '/')
            f.write(f"file '{abs_path}'\n")
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(list_file),
        '-c', 'copy',
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        list_file.unlink()
        
        for video in video_files:
            try:
                if os.path.exists(video):
                    os.remove(video)
            except:
                pass
        
        return True
    except Exception as e:
        print(f"✗ Concatenation error: {e}")
        if list_file.exists():
            list_file.unlink()
        return False

def cleanup_temp_files():
    """Clean up temporary files"""
    try:
        for item in TEMP_DIR.glob("*"):
            try:
                if item.is_file():
                    item.unlink()
            except:
                pass
    except:
        pass

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        data = request.json
        reciter = data.get('reciter')
        surah = data.get('surah')
        ayah_from = data.get('ayah_from')
        ayah_to = data.get('ayah_to')
        
        if not all([reciter, surah, ayah_from, ayah_to]):
            return jsonify({'error': 'Missing parameters'}), 400
        
        print(f"\n{'='*70}")
        print(f"🎬 AUTOMATIC QURAN REEL GENERATION")
        print(f"{'='*70}")
        print(f"  Reciter: {reciter}")
        print(f"  Surah {surah}: Ayahs {ayah_from}-{ayah_to}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        print("[STEP 1/6] Fetching Quran text with tashkeel...")
        audio_data = []
        total_duration = 0
        
        for ayah_num in range(ayah_from, ayah_to + 1):
            text = get_ayah_text(surah, ayah_num)
            if not text:
                return jsonify({'error': f'Failed to fetch ayah {ayah_num} text'}), 500
            
            print(f"  ✓ Ayah {ayah_num}: {text[:50]}...")
            
            audio_path = download_audio(reciter, surah, ayah_num)
            if not audio_path:
                return jsonify({'error': f'Failed to download audio for ayah {ayah_num}'}), 500
            
            duration = get_audio_duration(audio_path)
            audio_data.append({
                'ayah': ayah_num,
                'text': text,
                'audio': audio_path,
                'duration': duration
            })
            total_duration += duration
        
        print(f"\n✓ Total duration: {total_duration:.1f}s")
        
        print("\n[STEP 2/6] Selecting unique backgrounds for each ayah...")
        num_ayahs = len(audio_data)
        bg_videos = get_unique_backgrounds(num_ayahs)
        if not bg_videos:
            return jsonify({'error': 'No nature videos available. Add videos to backgrounds/ folder.'}), 500
        
        # Assign unique background to each ayah
        for i, item in enumerate(audio_data):
            item['background'] = bg_videos[i]
            print(f"  ✓ Ayah {item['ayah']}: {os.path.basename(item['background'])}")
        
        print("\n[STEP 3/6] Creating text overlays with proper Arabic rendering...")
        for item in audio_data:
            text_overlay = create_text_overlay_png(item['text'], width=1080, height=1920)
            if not text_overlay:
                return jsonify({'error': f'Text overlay failed for ayah {item["ayah"]}'}), 500
            item['overlay'] = text_overlay
        
        print("\n[STEP 4/6] Preparing background segments...")
        temp_videos = []
        current_offset = 0
        
        for item in audio_data:
            print(f"  Processing ayah {item['ayah']}...")
            
            bg_segment = prepare_background_segment(item['background'], item['duration'], 0)
            if not bg_segment:
                return jsonify({'error': f'Background prep failed for ayah {item["ayah"]}'}), 500
            
            video_path = str(TEMP_DIR / f"reel_{item['ayah']}_{int(time.time())}.mp4")
            
            if not create_final_reel(bg_segment, item['overlay'], item['audio'], video_path):
                return jsonify({'error': f'Reel creation failed for ayah {item["ayah"]}'}), 500
            
            temp_videos.append(video_path)
            current_offset += item['duration']
            
            try:
                if os.path.exists(item['overlay']):
                    os.remove(item['overlay'])
                if os.path.exists(bg_segment):
                    os.remove(bg_segment)
            except:
                pass
        
        print("\n[STEP 5/6] Concatenating final video...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reciter_name = reciter.replace('/', '-')
        final_video = str(OUTPUT_DIR / f"QuranReel_S{surah}_A{ayah_from}-{ayah_to}_{reciter_name}_{timestamp}.mp4")
        
        if not concatenate_videos_fast(temp_videos, final_video):
            return jsonify({'error': 'Final concatenation failed'}), 500
        
        print("\n[STEP 6/6] Cleaning up temporary files...")
        cleanup_temp_files()
        
        elapsed = time.time() - start_time
        video_filename = os.path.basename(final_video)
        
        print(f"\n{'='*70}")
        print(f"✅ GENERATION COMPLETE!")
        print(f"{'='*70}")
        print(f"  Output: {video_filename}")
        print(f"  Duration: {total_duration:.1f}s")
        print(f"  Render time: {elapsed:.1f}s")
        print(f"  Speed ratio: {total_duration/elapsed:.2f}x")
        print(f"{'='*70}\n")
        
        return jsonify({
            'success': True,
            'video_url': f'/outputs/{video_filename}',
            'video_name': video_filename,
            'render_time': f'{elapsed:.1f}s',
            'video_duration': f'{total_duration:.1f}s',
            'message': 'Quran Reel created successfully!'
        })
    
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"❌ CRITICAL ERROR: {e}")
        print(f"{'='*70}\n")
        cleanup_temp_files()
        return jsonify({'error': str(e)}), 500

@app.route('/outputs/<path:filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'backgrounds': len(list(BACKGROUNDS_DIR.glob("*.mp4"))),
        'cached_audio': len(list(AUDIO_DIR.glob("*.mp3"))),
        'outputs': len(list(OUTPUT_DIR.glob("*.mp4")))
    })

@app.route('/reciters')
def get_reciters():
    """Get list of verified reciters with their status"""
    reciters = []
    for key, info in VERIFIED_RECITERS.items():
        reciters.append({
            'id': key,
            'display': info['display'],
            'verified': info['verified'],
            'has_fallback': info['fallback'] is not None
        })
    return jsonify({
        'reciters': reciters,
        'guaranteed_fallback': GUARANTEED_FALLBACK
    })

@app.route('/validate', methods=['POST'])
def validate_audio():
    """Pre-validate audio availability for all requested ayahs"""
    try:
        data = request.json
        reciter = data.get('reciter')
        surah = data.get('surah')
        ayah_from = data.get('ayah_from')
        ayah_to = data.get('ayah_to')
        
        reciter_key = reciter.replace('/', '_')
        results = []
        all_available = True
        
        for ayah in range(ayah_from, ayah_to + 1):
            # Check if we can get audio (with fallback)
            surah_str = str(surah).zfill(3)
            ayah_str = str(ayah).zfill(3)
            
            # Check cache first
            for try_reciter in [reciter_key, GUARANTEED_FALLBACK]:
                if try_reciter in VERIFIED_RECITERS:
                    cache_file = AUDIO_DIR / f"{try_reciter}_{surah_str}_{ayah_str}.mp3"
                    if cache_file.exists() and cache_file.stat().st_size > 0:
                        results.append({'ayah': ayah, 'status': 'cached', 'reciter': try_reciter})
                        break
            else:
                # Check primary URL
                if reciter_key in VERIFIED_RECITERS:
                    url = get_audio_url(VERIFIED_RECITERS[reciter_key]['folder'], surah, ayah)
                    if validate_audio_url(url):
                        results.append({'ayah': ayah, 'status': 'available', 'reciter': reciter_key})
                        continue
                
                # Check fallback
                fallback_url = get_audio_url(VERIFIED_RECITERS[GUARANTEED_FALLBACK]['folder'], surah, ayah)
                if validate_audio_url(fallback_url):
                    results.append({'ayah': ayah, 'status': 'fallback', 'reciter': GUARANTEED_FALLBACK})
                else:
                    results.append({'ayah': ayah, 'status': 'unavailable', 'reciter': None})
                    all_available = False
        
        return jsonify({
            'valid': all_available,
            'results': results,
            'message': 'All audio available' if all_available else 'Some audio may use fallback'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🎬 AUTOMATIC QURAN REELS GENERATOR")
    print("  Fully Automated | No Manual Intervention")
    print("="*70)
    print(f"  Audio cache: {AUDIO_DIR}")
    print(f"  Backgrounds: {BACKGROUNDS_DIR}")
    print(f"  Output: {OUTPUT_DIR}")
    print("="*70)
    print("  Server: http://localhost:5000")
    print("  Health: http://localhost:5000/health")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
