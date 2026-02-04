# Test Arabic text rendering
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
import os

# Test text with tashkeel
text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"

print(f"Original text: {text}")
print(f"Text length: {len(text)}")

# Test reshaper with proper config
configuration = {
    'delete_harakat': False,
    'delete_tatweel': False,
    'support_zwj': True,
    'support_ligatures': True,
}
reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)
reshaped = reshaper.reshape(text)
bidi_text = get_display(reshaped)

print(f"Reshaped: {reshaped}")
print(f"Bidi: {bidi_text}")

# Create test image
fonts_dir = r"c:\Quran\fonts"
font_files = [
    os.path.join(fonts_dir, "Amiri-Regular.ttf"),
    os.path.join(fonts_dir, "ScheherazadeNew-Regular.ttf"),
]

for font_path in font_files:
    if os.path.exists(font_path):
        print(f"\nTesting font: {os.path.basename(font_path)}")
        
        img = Image.new('RGBA', (800, 200), (50, 50, 50, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, 60)
        
        # Draw the bidi text
        draw.text((400, 100), bidi_text, font=font, fill=(255, 255, 255), anchor="mm")
        
        output_path = os.path.join(fonts_dir, f"test_{os.path.basename(font_path)}.png")
        img.save(output_path)
        print(f"Saved: {output_path}")
