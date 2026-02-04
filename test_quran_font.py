# -*- coding: utf-8 -*-
"""
Quran Font Test Suite
Tests UthmanTNB_v2-0.ttf for proper rendering of Quranic text with full tashkeel.

⚠️ CRITICAL: This test MUST pass before any changes to the main project.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# Configuration
FONTS_DIR = Path(__file__).parent / "fonts"
FONT_FILE = FONTS_DIR / "UthmanTNB_v2-0.ttf"
OUTPUT_DIR = Path(__file__).parent / "test_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Test cases with various tashkeel combinations
TEST_CASES = [
    {
        "name": "shadda_fatha_alif",
        "text": "لَا يُكَلِّفُ ٱللَّهُ نَفۡسًا إِلَّا وُسۡعَهَا",
        "description": "Shadda + Fatha + Alif combinations"
    },
    {
        "name": "hamd_lillah",
        "text": "ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ",
        "description": "Basic Fatiha verse with madd"
    },
    {
        "name": "ghafilan",
        "text": "وَلَا تَحۡسَبَنَّ ٱللَّهَ غَٰفِلًا",
        "description": "Tanween + special alif"
    },
    {
        "name": "bismillah",
        "text": "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ",
        "description": "Bismillah with all diacritics"
    },
    {
        "name": "ayat_kursi_part",
        "text": "ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلۡحَيُّ ٱلۡقَيُّومُ",
        "description": "Ayat al-Kursi opening with hamzat"
    },
    {
        "name": "sukoon_test",
        "text": "قُلۡ هُوَ ٱللَّهُ أَحَدٌ",
        "description": "Sukoon and tanween"
    },
    {
        "name": "madd_test",
        "text": "وَٱلسَّمَآءِ ذَاتِ ٱلۡبُرُوجِ",
        "description": "Madd marks"
    },
    {
        "name": "long_ayah",
        "text": "وَإِذَا قِيلَ لَهُمۡ لَا تُفۡسِدُواْ فِي ٱلۡأَرۡضِ قَالُوٓاْ إِنَّمَا نَحۡنُ مُصۡلِحُونَ",
        "description": "Long ayah spanning multiple lines"
    }
]

def validate_font():
    """Check if font file exists and is valid"""
    if not FONT_FILE.exists():
        print(f"❌ CRITICAL ERROR: Font not found: {FONT_FILE}")
        return False
    
    try:
        font = ImageFont.truetype(str(FONT_FILE), 60)
        print(f"✅ Font loaded successfully: {FONT_FILE.name}")
        return True
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Cannot load font: {e}")
        return False

def reshape_arabic(text):
    """Apply arabic_reshaper + bidi - ONE TIME ONLY before render"""
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    return bidi_text

def render_test_image(test_case, font_size=65):
    """Render a single test case to image"""
    name = test_case["name"]
    text = test_case["text"]
    description = test_case["description"]
    
    # Create image
    width = 1080
    height = 400
    img = Image.new('RGB', (width, height), color='#1a2744')
    draw = ImageDraw.Draw(img)
    
    # Load font
    try:
        font = ImageFont.truetype(str(FONT_FILE), font_size)
        label_font = ImageFont.truetype(str(FONT_FILE), 24)
    except Exception as e:
        print(f"❌ Font load error for {name}: {e}")
        return False
    
    # Process text (reshape + bidi)
    processed_text = reshape_arabic(text)
    
    # Draw label
    draw.text((width - 40, 30), description, font=label_font, fill='#a0aec0', anchor='ra')
    
    # Calculate text position (centered)
    try:
        bbox = draw.textbbox((0, 0), processed_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    except:
        x = width // 2
        y = height // 2
    
    # Draw shadow
    shadow_offset = 3
    draw.text((x + shadow_offset, y + shadow_offset), processed_text, 
              font=font, fill='#000000')
    
    # Draw main text
    draw.text((x, y), processed_text, font=font, fill='#ffffff')
    
    # Save image
    output_path = OUTPUT_DIR / f"test_{name}.png"
    img.save(output_path, 'PNG')
    print(f"✅ Generated: {output_path.name}")
    
    return True

def create_combined_test_image():
    """Create a single image with all test cases"""
    width = 1080
    row_height = 180
    num_tests = len(TEST_CASES)
    height = row_height * num_tests + 100
    
    img = Image.new('RGB', (width, height), color='#0f1729')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(str(FONT_FILE), 55)
        title_font = ImageFont.truetype(str(FONT_FILE), 32)
    except Exception as e:
        print(f"❌ Font load error: {e}")
        return False
    
    # Title
    title = reshape_arabic("اختبار خط المصحف - UthmanTNB")
    draw.text((width // 2, 40), title, font=title_font, fill='#7c8cc4', anchor='mm')
    
    # Draw each test
    y_offset = 100
    for i, test_case in enumerate(TEST_CASES):
        text = test_case["text"]
        processed_text = reshape_arabic(text)
        
        # Background stripe
        stripe_color = '#1a2744' if i % 2 == 0 else '#1e2d4a'
        draw.rectangle([0, y_offset, width, y_offset + row_height], fill=stripe_color)
        
        # Draw text centered
        try:
            bbox = draw.textbbox((0, 0), processed_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
        except:
            x = width // 2
        
        # Shadow
        draw.text((x + 2, y_offset + row_height // 2 + 2), processed_text, 
                  font=font, fill='#000000', anchor='lm')
        # Main text
        draw.text((x, y_offset + row_height // 2), processed_text, 
                  font=font, fill='#ffffff', anchor='lm')
        
        y_offset += row_height
    
    # Save
    output_path = OUTPUT_DIR / "quran_font_test_suite.png"
    img.save(output_path, 'PNG')
    print(f"\n✅ Combined test image saved: {output_path}")
    
    return str(output_path)

def run_all_tests():
    """Run the complete test suite"""
    print("=" * 70)
    print("  🕌 QURAN FONT TEST SUITE - UthmanTNB_v2-0.ttf")
    print("  ⚠️  This test MUST pass before project deployment")
    print("=" * 70)
    
    # Step 1: Validate font
    print("\n📋 STEP 1: Font Validation")
    if not validate_font():
        print("\n❌ TEST FAILED: Font validation failed")
        return False
    
    # Step 2: Render individual tests
    print("\n📋 STEP 2: Individual Test Cases")
    all_passed = True
    for test_case in TEST_CASES:
        success = render_test_image(test_case)
        if not success:
            all_passed = False
    
    # Step 3: Combined test image
    print("\n📋 STEP 3: Combined Test Image")
    combined_path = create_combined_test_image()
    
    # Summary
    print("\n" + "=" * 70)
    if all_passed:
        print("  ✅ ALL TESTS PASSED")
        print(f"  📂 Output: {OUTPUT_DIR}")
        print("\n  ⚠️  MANUAL VERIFICATION REQUIRED:")
        print("  - Check for letter connections")
        print("  - Verify tashkeel positioning")
        print("  - Confirm no overlapping/clipping")
        print("  - Compare with Mushaf")
    else:
        print("  ❌ SOME TESTS FAILED")
        print("  ⛔ DO NOT proceed with project changes")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
