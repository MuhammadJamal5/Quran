# -*- coding: utf-8 -*-
"""
Font Compatibility Test - Find the font that renders connected Arabic properly
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

FONTS_DIR = Path("fonts")
OUTPUT_DIR = Path("test_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Test verse
TEST_VERSE = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"

print("=" * 80)
print("FONT COMPATIBILITY TEST")
print("=" * 80)
print(f"Test: {TEST_VERSE}")

# Configure reshaper
reshaper = arabic_reshaper.ArabicReshaper(configuration={
    'delete_harakat': False,
    'delete_tatweel': False,
    'support_zwj': True,
    'support_ligatures': True,
})

# Test different fonts
fonts_to_test = []
for font_file in FONTS_DIR.glob("*.ttf"):
    fonts_to_test.append(font_file)
for font_file in FONTS_DIR.glob("*.otf"):
    fonts_to_test.append(font_file)

print(f"Found {len(fonts_to_test)} fonts to test")

# Create comparison image
width = 1080
row_height = 150
height = len(fonts_to_test) * row_height + 200
img = Image.new('RGB', (width, height), color='#0a1628')
draw = ImageDraw.Draw(img)

# Title
draw.text((width//2, 50), "Font Comparison - Connected Letters Test", 
          font=ImageFont.load_default(), fill='#ffffff', anchor='mm')

y = 120

# Test each font
for font_file in fonts_to_test:
    try:
        font = ImageFont.truetype(str(font_file), 48)
        
        # Process text
        reshaped = reshaper.reshape(TEST_VERSE)
        bidi_text = get_display(reshaped)
        
        # Font name
        draw.text((50, y), font_file.name[:30], font=ImageFont.load_default(), fill='#7c8cc4')
        
        # Rendered text
        draw.text((width//2, y + 30), bidi_text, font=font, fill='#ffffff', anchor='mm',
                  stroke_width=2, stroke_fill='#000000')
        
        print(f"✓ {font_file.name}: Rendered")
        
    except Exception as e:
        draw.text((50, y), f"{font_file.name}: ERROR - {str(e)[:40]}", 
                  font=ImageFont.load_default(), fill='#ff6666')
        print(f"✗ {font_file.name}: {e}")
    
    y += row_height

# Also test WITHOUT reshaper (raw bidi only)
y += 20
draw.text((50, y), "=== NO RESHAPER (raw bidi) ===", font=ImageFont.load_default(), fill='#ffcc00')
y += 30

for font_file in fonts_to_test[:3]:  # Just first 3
    try:
        font = ImageFont.truetype(str(font_file), 48)
        bidi_only = get_display(TEST_VERSE)  # NO reshaping
        draw.text((width//2, y), bidi_only, font=font, fill='#ffffff', anchor='mm')
        draw.text((50, y), font_file.name[:20], font=ImageFont.load_default(), fill='#7c8cc4')
        y += row_height
    except:
        pass

# Save
output_path = OUTPUT_DIR / "font_comparison.png"
img.save(output_path, 'PNG')
print(f"\n✅ Saved: {output_path}")
print("=" * 80)
