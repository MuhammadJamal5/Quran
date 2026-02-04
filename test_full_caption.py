# -*- coding: utf-8 -*-
"""
Create proper Quran caption test - Full size like actual reel
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

FONT_FILE = Path("fonts/UthmanTNB_v2-0.ttf")
OUTPUT_DIR = Path("test_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Test verses - same ones that appear broken
VERSES = [
    "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ",
    "ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ",
    "ذَٰلِكَ ٱلۡكِتَٰبُ لَا رَيۡبَ فِيهِ هُدٗى لِّلۡمُتَّقِينَ",
]

print("=" * 80)
print("FULL CAPTION TEST - Simulating Real Reel")
print("=" * 80)

# Configure reshaper
reshaper = arabic_reshaper.ArabicReshaper(configuration={
    'delete_harakat': False,
    'delete_tatweel': False,
    'support_zwj': True,
    'support_ligatures': True,
})

def shape_text(text):
    reshaped = reshaper.reshape(text)
    return get_display(reshaped)

# Create reel-size image
width = 1080
height = 1920
img = Image.new('RGB', (width, height), color='#1a2744')
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(str(FONT_FILE), 80)
small_font = ImageFont.truetype(str(FONT_FILE), 40)

# Title
draw.text((width//2, 100), "اختبار النص القرآني", font=small_font, fill='#7c8cc4', anchor='mm')

# Center the verses
y = 500
line_spacing = 200

for verse in VERSES:
    # Count tashkeel
    tashkeel_before = sum(1 for c in verse if 0x064B <= ord(c) <= 0x0652)
    
    # Process
    shaped = shape_text(verse)
    
    tashkeel_after = sum(1 for c in shaped if 0x064B <= ord(c) <= 0x0652)
    
    # Draw with stroke
    draw.text((width//2, y), shaped, font=font, fill='#ffffff', anchor='mm',
              stroke_width=3, stroke_fill='#000000')
    
    print(f"Verse: {tashkeel_before}→{tashkeel_after} tashkeel")
    
    y += line_spacing

# Footer
draw.text((width//2, height - 150), f"Font: UthmanTNB_v2-0.ttf", 
          font=ImageFont.load_default(), fill='#666666', anchor='mm')

# Save
output_path = OUTPUT_DIR / "full_caption_test.png"
img.save(output_path, 'PNG')
print(f"\n✅ Saved: {output_path}")
print("=" * 80)
