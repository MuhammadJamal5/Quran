# -*- coding: utf-8 -*-
"""
QURAN CAPTION DIAGNOSTIC - Deep Investigation
Identifies the EXACT root cause of broken Arabic rendering.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import unicodedata

FONT_FILE = Path("fonts/UthmanTNB_v2-0.ttf")
OUTPUT_DIR = Path("test_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Test verse with complex tashkeel
TEST_VERSE = "ذَٰلِكَ ٱلۡكِتَٰبُ لَا رَيۡبَ ۛ فِيهِ ۛ هُدٗى لِّلۡمُتَّقِينَ"

print("=" * 80)
print("QURAN CAPTION DIAGNOSTIC - Deep Investigation")
print("=" * 80)

# ============================================================================
# STEP 1: Analyze the raw Unicode
# ============================================================================
print("\n📋 STEP 1: Unicode Analysis")
print("-" * 40)

print(f"Original text: {TEST_VERSE}")
print(f"Length: {len(TEST_VERSE)} characters")

# Count character types
arabic_letters = 0
tashkeel = 0
special_marks = 0
spaces = 0
other = 0

for char in TEST_VERSE:
    code = ord(char)
    if 0x0621 <= code <= 0x063A or 0x0641 <= code <= 0x064A:  # Arabic letters
        arabic_letters += 1
    elif 0x064B <= code <= 0x0652:  # Tashkeel
        tashkeel += 1
    elif 0x0610 <= code <= 0x061A or 0x06D6 <= code <= 0x06ED:  # Quranic marks
        special_marks += 1
    elif char == ' ':
        spaces += 1
    else:
        other += 1

print(f"Arabic letters: {arabic_letters}")
print(f"Tashkeel (harakat): {tashkeel}")
print(f"Quranic special marks: {special_marks}")
print(f"Spaces: {spaces}")
print(f"Other: {other}")

# Unicode normalization test
print("\n📋 STEP 2: Unicode Normalization Test")
print("-" * 40)

nfc = unicodedata.normalize('NFC', TEST_VERSE)
nfkc = unicodedata.normalize('NFKC', TEST_VERSE)

print(f"Original == NFC: {TEST_VERSE == nfc}")
print(f"Original == NFKC: {TEST_VERSE == nfkc}")
print(f"NFC length: {len(nfc)}")
print(f"NFKC length: {len(nfkc)}")

# ============================================================================
# STEP 3: Test different reshaper configurations
# ============================================================================
print("\n📋 STEP 3: Arabic Reshaper Configurations")
print("-" * 40)

configs = [
    ("Default (deletes harakat)", {}),
    ("Preserve harakat", {'delete_harakat': False}),
    ("Preserve all", {
        'delete_harakat': False,
        'delete_tatweel': False,
        'support_zwj': True,
        'support_ligatures': True,
    }),
]

for name, config in configs:
    if config:
        reshaper = arabic_reshaper.ArabicReshaper(configuration=config)
        reshaped = reshaper.reshape(TEST_VERSE)
    else:
        reshaped = arabic_reshaper.reshape(TEST_VERSE)
    
    tashkeel_count = sum(1 for c in reshaped if 0x064B <= ord(c) <= 0x0652)
    print(f"{name}:")
    print(f"  Tashkeel preserved: {tashkeel_count}")
    print(f"  Length: {len(reshaped)}")

# ============================================================================
# STEP 4: Visual rendering comparison
# ============================================================================
print("\n📋 STEP 4: Visual Rendering Comparison")
print("-" * 40)

width = 1080
height = 1600
img = Image.new('RGB', (width, height), color='#0a1628')
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype(str(FONT_FILE), 48)
    small_font = ImageFont.truetype(str(FONT_FILE), 24)
except Exception as e:
    print(f"❌ Font load failed: {e}")
    sys.exit(1)

y = 50

# Title
draw.text((width//2, y), "Quran Caption Diagnostic", font=small_font, fill='#7c8cc4', anchor='mm')
y += 60

# Test cases
test_cases = [
    ("1. Raw text (no processing)", TEST_VERSE),
    ("2. Bidi only", get_display(TEST_VERSE)),
    ("3. Reshaper only (default)", arabic_reshaper.reshape(TEST_VERSE)),
    ("4. Reshaper (preserve) + Bidi", None),  # Will compute below
    ("5. NFC normalized + Reshaper + Bidi", None),
]

# Compute case 4
reshaper_preserve = arabic_reshaper.ArabicReshaper(configuration={
    'delete_harakat': False,
    'delete_tatweel': False,
    'support_zwj': True,
    'support_ligatures': True,
})
case4_reshaped = reshaper_preserve.reshape(TEST_VERSE)
case4_bidi = get_display(case4_reshaped)
test_cases[3] = ("4. Reshaper (preserve) + Bidi", case4_bidi)

# Compute case 5
nfc_text = unicodedata.normalize('NFC', TEST_VERSE)
case5_reshaped = reshaper_preserve.reshape(nfc_text)
case5_bidi = get_display(case5_reshaped)
test_cases[4] = ("5. NFC + Reshaper (preserve) + Bidi", case5_bidi)

for label, text in test_cases:
    # Label
    draw.text((width - 50, y), label, font=small_font, fill='#a0aec0', anchor='ra')
    y += 40
    
    # Text with stroke
    draw.text((width//2, y), text, font=font, fill='#ffffff', anchor='mm',
              stroke_width=2, stroke_fill='#000000')
    y += 100
    
    # Count tashkeel
    tashkeel_count = sum(1 for c in text if 0x064B <= ord(c) <= 0x0652)
    print(f"{label}: {tashkeel_count} tashkeel")

# ============================================================================
# STEP 5: Character-by-character analysis of the CORRECT method
# ============================================================================
print("\n📋 STEP 5: Correct Pipeline Analysis")
print("-" * 40)

print("CORRECT PIPELINE:")
print("  1. Get Uthmani text from API (already has tashkeel)")
print("  2. Apply arabic_reshaper with delete_harakat=False")
print("  3. Apply bidi.get_display()")
print("  4. Render with Quran-compatible font")
print()
print(f"Before reshaper: {len(TEST_VERSE)} chars, {tashkeel} tashkeel")
print(f"After reshaper:  {len(case4_reshaped)} chars, {sum(1 for c in case4_reshaped if 0x064B <= ord(c) <= 0x0652)} tashkeel")
print(f"After bidi:      {len(case4_bidi)} chars, {sum(1 for c in case4_bidi if 0x064B <= ord(c) <= 0x0652)} tashkeel")

# Save diagnostic image
output_path = OUTPUT_DIR / "caption_diagnostic.png"
img.save(output_path, 'PNG')
print(f"\n✅ Diagnostic image saved: {output_path}")

# ============================================================================
# STEP 6: Identify the problem
# ============================================================================
print("\n" + "=" * 80)
print("📊 DIAGNOSIS SUMMARY")
print("=" * 80)

# Check if default reshaper removes tashkeel
default_reshaped = arabic_reshaper.reshape(TEST_VERSE)
default_tashkeel = sum(1 for c in default_reshaped if 0x064B <= ord(c) <= 0x0652)

if default_tashkeel == 0:
    print("⚠️  ROOT CAUSE IDENTIFIED: arabic_reshaper.reshape() DELETES tashkeel by default!")
    print("    The default configuration has delete_harakat=True")
    print()
    print("✅ FIX: Use ArabicReshaper with configuration={'delete_harakat': False}")
else:
    print("✓ Tashkeel preserved in reshaper")

# Check if preserved reshaper works
preserved_tashkeel = sum(1 for c in case4_bidi if 0x064B <= ord(c) <= 0x0652)
if preserved_tashkeel == tashkeel:
    print(f"✅ Preserved reshaper keeps all {tashkeel} tashkeel marks")
else:
    print(f"⚠️  Preserved reshaper: {preserved_tashkeel}/{tashkeel} tashkeel")

print()
print("=" * 80)
