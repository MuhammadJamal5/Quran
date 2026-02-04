# -*- coding: utf-8 -*-
import sys
import os
from bidi.algorithm import get_display

# Ensure we can import main
sys.path.append(os.getcwd())
from main import create_text_overlay_png, get_quran_reshaper

print("Verifying main.py logic...")

text = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
expected_tashkeel = sum(1 for c in text if 0x064B <= ord(c) <= 0x0652)
print(f"Original tashkeel: {expected_tashkeel}")

# 1. Verify reshaper logic accessible via main.py
reshaper = get_quran_reshaper()
reshaped = reshaper.reshape(text)
bidi_text = get_display(reshaped)

actual_tashkeel = sum(1 for c in bidi_text if 0x064B <= ord(c) <= 0x0652)
print(f"Processed tashkeel: {actual_tashkeel}")

if actual_tashkeel == expected_tashkeel:
    print("✅ Reshaper logic PASS: Tashkeel preserved")
else:
    print(f"❌ Reshaper logic FAIL: Expected {expected_tashkeel}, got {actual_tashkeel}")

# 2. Verify image generation
print("Generating test image...")
path = create_text_overlay_png(text)
if path:
    print(f"✅ Image generation PASS: {path}")
else:
    print("❌ Image generation FAIL")
