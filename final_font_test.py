# -*- coding: utf-8 -*-
"""
Final Quran Font Validation - Ready for Production
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

FONT_FILE = Path("fonts/UthmanTNB_v2-0.ttf")
OUTPUT_DIR = Path("test_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Comprehensive test verses with all tashkeel types
TEST_VERSES = [
    ("البسملة", "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"),
    ("الفاتحة", "ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ"),
    ("آية الكرسي", "ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلۡحَيُّ ٱلۡقَيُّومُ"),
    ("الإخلاص", "قُلۡ هُوَ ٱللَّهُ أَحَدٌ"),
    ("آية طويلة", "لَا يُكَلِّفُ ٱللَّهُ نَفۡسًا إِلَّا وُسۡعَهَا"),
]

print("=" * 70)
print("  🕌 FINAL QURAN FONT PRODUCTION TEST")
print("  Font: UthmanTNB_v2-0.ttf (EXCLUSIVE)")
print("=" * 70)

# Configure reshaper - PRESERVE ALL TASHKEEL
reshaper = arabic_reshaper.ArabicReshaper(configuration={
    'delete_harakat': False,
    'delete_tatweel': False,
    'support_ligatures': True,
    'support_zwj': True,
})

def reshape_quran(text):
    """Process Quran text - ONE TIME ONLY before render"""
    reshaped = reshaper.reshape(text)
    return get_display(reshaped)

# Create production-quality test image
width = 1080
height = 1920
img = Image.new('RGB', (width, height), color='#0a1628')
draw = ImageDraw.Draw(img)

try:
    quran_font = ImageFont.truetype(str(FONT_FILE), 58)
    title_font = ImageFont.truetype(str(FONT_FILE), 32)
    label_font = ImageFont.truetype(str(FONT_FILE), 22)
except Exception as e:
    print(f"❌ FONT LOAD FAILED: {e}")
    exit(1)

# Background overlay effect
for y in range(height):
    alpha = int(20 + (y / height) * 30)
    draw.rectangle([0, y, width, y+1], fill=(10, 22, 40))

# Title
title = reshape_quran("اختبار الفونت النهائي - جاهز للإنتاج")
draw.text((width // 2, 80), title, font=title_font, fill='#7c8cc4', anchor='mm')

# Subtitle
subtitle = "UthmanTNB_v2-0.ttf"
draw.text((width // 2, 130), subtitle, font=label_font, fill='#4a5568', anchor='mm')

# Render each test verse
y_pos = 250
spacing = 300

for label_ar, verse in TEST_VERSES:
    # Label
    label_processed = reshape_quran(label_ar)
    draw.text((width - 80, y_pos - 60), label_processed, font=label_font, fill='#a0aec0', anchor='ra')
    
    # Verse with shadow
    verse_processed = reshape_quran(verse)
    
    # Strong shadow for readability
    for offset in [(3, 3), (2, 2), (1, 1)]:
        shadow_alpha = 150 - offset[0] * 30
        draw.text((width // 2 + offset[0], y_pos + offset[1]), verse_processed, 
                  font=quran_font, fill='#000000', anchor='mm')
    
    # Main text
    draw.text((width // 2, y_pos), verse_processed, font=quran_font, fill='#ffffff', anchor='mm')
    
    # Tashkeel count
    tashkeel_count = sum(1 for c in verse if 0x064B <= ord(c) <= 0x0652)
    processed_count = sum(1 for c in verse_processed if 0x064B <= ord(c) <= 0x0652)
    status = "✅" if tashkeel_count == processed_count else "⚠️"
    print(f"  {label_ar}: {tashkeel_count} tashkeel → {processed_count} processed {status}")
    
    y_pos += spacing

# Footer
footer = reshape_quran("صدقة جارية - كل سنة وأنتم طيبين 🌙")
draw.text((width // 2, height - 100), footer, font=label_font, fill='#4a5568', anchor='mm')

# Save
output_path = OUTPUT_DIR / "production_ready_test.png"
img.save(output_path, 'PNG', quality=95)

print(f"\n✅ Production test saved: {output_path}")
print("=" * 70)
