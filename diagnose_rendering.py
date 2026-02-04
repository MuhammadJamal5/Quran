import ctypes
from ctypes import wintypes
import os
from pathlib import Path
from PIL import Image

# --- GDI DEFINITIONS (STRICTLY COPIED FROM RENDERER) ---
gdi32 = ctypes.windll.gdi32
user32 = ctypes.windll.user32

FR_PRIVATE = 0x10
ANSI_CHARSET = 0
DEFAULT_CHARSET = 1
ARABIC_CHARSET = 178
FW_NORMAL = 400
OUT_TT_PRECIS = 4
CLIP_DEFAULT_PRECIS = 0
ANTIALIASED_QUALITY = 4
CLEARTYPE_QUALITY = 5
DEFAULT_PITCH = 0
FF_DONTCARE = 0
DT_CENTER = 1
DT_RTLREADING = 0x00020000
DT_WORDBREAK = 0x00000010
DT_NOPREFIX = 0x00000800
TRANSPARENT = 1

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG),
                ("biPlanes", wintypes.WORD), ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG), ("biYPelsPerMeter", wintypes.LONG),
                ("biClrUsed", wintypes.DWORD), ("biClrImportant", wintypes.DWORD)]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3)]

def render_test(text, font_path, font_name, output_file):
    print(f"--- DIAGNOSTIC RENDER FOR: {font_name} ---")
    
    # 1. Load Font
    ret = gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
    print(f"AddFontResourceExW: {ret} (Should be > 0)")
    
    # 2. Setup GDI
    width, height = 800, 300
    hwin = user32.GetDesktopWindow()
    hdc_screen = user32.GetDC(hwin)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    hbitmap = gdi32.CreateCompatibleBitmap(hdc_screen, width, height)
    old_bitmap = gdi32.SelectObject(hdc_mem, hbitmap)
    
    # Fill Black
    bk_rect = wintypes.RECT(0, 0, width, height)
    fill_brush = gdi32.GetStockObject(4) # BLACK_BRUSH
    user32.FillRect(hdc_mem, ctypes.byref(bk_rect), fill_brush)
    
    # 3. Create Font (STRICT ARABIC CONFIG)
    lfHeight = -100
    hfont = gdi32.CreateFontW(
        lfHeight, 0, 0, 0, FW_NORMAL, 0, 0, 0, 
        ARABIC_CHARSET, # Critical
        OUT_TT_PRECIS, CLIP_DEFAULT_PRECIS, 
        CLEARTYPE_QUALITY, # Quality
        DEFAULT_PITCH | FF_DONTCARE, 
        font_name
    )
    old_font = gdi32.SelectObject(hdc_mem, hfont)
    
    # 4. Draw Text
    gdi32.SetBkMode(hdc_mem, TRANSPARENT)
    gdi32.SetTextColor(hdc_mem, 0x00FFFFFF)
    
    rect = wintypes.RECT(50, 50, width-50, height-50)
    flags = DT_CENTER | DT_WORDBREAK | DT_RTLREADING | DT_NOPREFIX
    
    ret_draw = user32.DrawTextW(hdc_mem, text, -1, ctypes.byref(rect), flags)
    print(f"DrawTextW Result (Height): {ret_draw}")
    
    # 5. Save to Image
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    
    buffer = ctypes.create_string_buffer(width * height * 4)
    gdi32.GetDIBits(hdc_mem, hbitmap, 0, height, buffer, ctypes.byref(bmi), 0)
    
    img = Image.frombytes("RGBA", (width, height), buffer.raw, "raw", "BGRA")
    
    # Cleanup
    gdi32.RemoveFontResourceExW(font_path, FR_PRIVATE, 0)
    gdi32.SelectObject(hdc_mem, old_bitmap)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteObject(hfont)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(hwin, hdc_screen)
    
    # Save
    img.save(output_file)
    print(f"Saved diagnostic image to: {output_file}")
    return output_file

if __name__ == "__main__":
    font_path = r"c:\Quran\fonts\Amiri-Quran.ttf"
    font_name = "Amiri" # Amiri Regular internal name is "Amiri"
    text = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ" # Uthmani Basmalah
    
    try:
        render_test(text, font_path, font_name, "test_render.png")
    except Exception as e:
        print(f"Render failed: {e}")
