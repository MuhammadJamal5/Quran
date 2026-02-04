# -*- coding: utf-8 -*-
"""
Tashkeel Fix - Configure arabic_reshaper to preserve diacritics
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

FONT_FILE = Path("fonts/UthmanTNB_v2-0.ttf")

# Uthmani Quran text WITH full tashkeel
TEST_VERSES = [
    "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ",
    "ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ",
    "لَا يُكَلِّفُ ٱللَّهُ نَفۡسًا إِلَّا وُسۡعَهَا",
]

print("=" * 70)
print("TASHKEEL FIX - Preserving Harakat")
print("=" * 70)

# Configure reshaper to PRESERVE harakat (tashkeel)
reshaper_config = arabic_reshaper.ArabicReshaper(configuration={
    'delete_harakat': False,
    'delete_tatweel': False,
    'support_ligatures': True,
    'support_zwj': True,
    'RIAL SIGN': True,
})

def reshape_with_tashkeel(text):
    """Reshape Arabic while PRESERVING tashkeel"""
    reshaped = reshaper_config.reshape(text)
    bidi_text = get_display(reshaped)
    return bidi_text

# Test
for i, verse in enumerate(TEST_VERSES):
    print(f"\nVerse {i+1}:")
    print(f"  Original:  {verse}")
    
    # Count tashkeel before
    tashkeel_before = sum(1 for c in verse if 0x064B <= ord(c) <= 0x0652)
    
    processed = reshape_with_tashkeel(verse)
    print(f"  Processed: {processed}")
    
    # Count tashkeel after
    tashkeel_after = sum(1 for c in processed if 0x064B <= ord(c) <= 0x0652)
    
    if tashkeel_after == tashkeel_before:
        print(f"  ✅ Tashkeel preserved: {tashkeel_before} → {tashkeel_after}")
    else:
        print(f"  ⚠️ Tashkeel count: {tashkeel_before} → {tashkeel_after}")

# Create visual test
print("\n" + "=" * 70)
print("Creating visual test...")

width = 1080
height = 500
img = Image.new('RGB', (width, height), color='#0f1729')
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(str(FONT_FILE), 50)
title_font = ImageFont.truetype(str(FONT_FILE), 28)

# Title
title = reshape_with_tashkeel("اختبار حفظ التشكيل")
draw.text((width // 2, 40), title, font=title_font, fill='#7c8cc4', anchor='mm')

y = 120
for verse in TEST_VERSES:
    processed = reshape_with_tashkeel(verse)
    
    # Shadow
    draw.text((width // 2 + 2, y + 2), processed, font=font, fill='#000000', anchor='mm')
    # Main
    draw.text((width // 2, y), processed, font=font, fill='#ffffff', anchor='mm')
    y += 120

output_path = Path("test_output/tashkeel_fixed.png")
img.save(output_path, 'PNG')
print(f"✅ Saved: {output_path}")
print("=" * 70)
