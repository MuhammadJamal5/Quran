
import ctypes
from ctypes import wintypes
import struct
from PIL import Image

# Windows GDI Constants
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20

FW_NORMAL = 400
FW_BOLD = 700

ANSI_CHARSET = 0
DEFAULT_CHARSET = 1
ARABIC_CHARSET = 178

OUT_DEFAULT_PRECIS = 0
OUT_TT_PRECIS = 4

CLIP_DEFAULT_PRECIS = 0

DEFAULT_QUALITY = 0
ANTIALIASED_QUALITY = 4
CLEARTYPE_QUALITY = 5

DEFAULT_PITCH = 0
FF_DONTCARE = 0

DT_CENTER = 0x00000001
DT_VCENTER = 0x00000004
DT_WORDBREAK = 0x00000010
DT_NOCLIP = 0x00000100
DT_RTLREADING = 0x00020000  # Important for Arabic
DT_NOPREFIX = 0x00000800

TRANSPARENT = 1
OPAQUE = 2

SRCCOPY = 0x00CC0020

# Structures
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3),
    ]

# Libraries
gdi32 = ctypes.windll.gdi32
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def load_private_font(font_path):
    """Load a font file privately for this process."""
    if not isinstance(font_path, str):
        font_path = str(font_path)
    
    # AddFontResourceExW returns number of fonts added
    ret = gdi32.AddFontResourceExW(font_path, FR_PRIVATE | FR_NOT_ENUM, 0)
    if ret == 0:
        print(f"[ERROR] AddFontResourceEx failed for {font_path}")
        return False
    return True

def render_text_to_image(text, font_name, font_size, width, height, text_color=(255, 255, 255)):
    """
    Render text using Windows GDI to a PIL Image.
    This handles complex scripts (Arabic) natively with correct shaping and GPOS.
    """
    
    # 1. Create Device Contexts
    hwin = user32.GetDesktopWindow()
    hdc_screen = user32.GetDC(hwin)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    
    # 2. Create Bitmap
    hbitmap = gdi32.CreateCompatibleBitmap(hdc_screen, width, height)
    old_bitmap = gdi32.SelectObject(hdc_mem, hbitmap)
    
    # 3. Create Font
    # Height = -MulDiv(PointSize, GetDeviceCaps(hDC, LOGPIXELSY), 72)
    # Approx: height in pixels
    
    # Note: UthmanTNB might need large size
    lfHeight = -int(font_size) 
    
    hfont = gdi32.CreateFontW(
        lfHeight, 0, 0, 0, 
        FW_NORMAL, 0, 0, 0, 
        ARABIC_CHARSET, 
        OUT_TT_PRECIS, 
        CLIP_DEFAULT_PRECIS, 
        ANTIALIASED_QUALITY, 
        DEFAULT_PITCH | FF_DONTCARE, 
        font_name
    )
    
    old_font = gdi32.SelectObject(hdc_mem, hfont)
    
    # 4. Setup Graphics
    # Clear background (Transparent is easier if we use black bg then convert to alpha?)
    # GDI DrawText doesn't handle Alpha channel in RGB easily.
    # Approach: Draw white text on black background. Use result as Alpha mask?
    # Or text_color on transparent?
    # Simple approach: Draw text on black. Luma = Alpha.
    
    # Fill Black
    bk_rect = wintypes.RECT(0, 0, width, height)
    # GetStockObject(BLACK_BRUSH) = 4
    fill_brush = gdi32.GetStockObject(4) 
    user32.FillRect(hdc_mem, ctypes.byref(bk_rect), fill_brush)
    
    # Set Text properties
    gdi32.SetBkMode(hdc_mem, TRANSPARENT)
    gdi32.SetTextColor(hdc_mem, 0x00FFFFFF) # White BGR
    
    # Calculate vertical position
    # DT_VCENTER only works with DT_SINGLELINE. For multiline, we must measure.
    rect_measure = wintypes.RECT(10, 10, width - 10, height - 10) # Initial constraints
    flags_base = DT_CENTER | DT_WORDBREAK | DT_RTLREADING | DT_NOPREFIX
    
    # Measure
    gdi32.SetBkMode(hdc_mem, TRANSPARENT) # Ensure setup
    gdi32.SetTextColor(hdc_mem, 0x00FFFFFF)
    
    # Copy rect for measurement
    rect_calc = wintypes.RECT(rect_measure.left, rect_measure.top, rect_measure.right, rect_measure.bottom)
    user32.DrawTextW(hdc_mem, text, -1, ctypes.byref(rect_calc), flags_base | 0x00000400) # DT_CALCRECT = 0x400
    
    text_height = rect_calc.bottom - rect_calc.top
    avail_height = height - 20 # Margins
    
    y_offset = (avail_height - text_height) // 2
    if y_offset < 0: y_offset = 0
    
    # Final Draw
    rect_draw = wintypes.RECT(rect_measure.left, 10 + y_offset, rect_measure.right, 10 + y_offset + text_height)
    user32.DrawTextW(hdc_mem, text, -1, ctypes.byref(rect_draw), flags_base)
    
    # 6. Extract Bits
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height # Top-down
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = 0 # BI_RGB
    
    buffer = ctypes.create_string_buffer(width * height * 4)
    gdi32.GetDIBits(hdc_mem, hbitmap, 0, height, buffer, ctypes.byref(bmi), 0)
    
    # 7. Create PIL Image
    # Image is BGRA (on little endian Windows 32-bit bitmap)
    try:
        image = Image.frombytes("RGBA", (width, height), buffer.raw, "raw", "BGRA")
    except:
        # Fallback if mode differs
        image = Image.frombytes("RGB", (width, height), buffer.raw, "raw", "BGRX")
    
    # 8. Cleanup
    gdi32.SelectObject(hdc_mem, old_bitmap)
    gdi32.SelectObject(hdc_mem, old_font)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteObject(hfont)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(hwin, hdc_screen)
    
    # Post-processing:
    # We drew white text on black.
    # Convert to user color with transparency.
    # Take the Blue channel (or Grayscale) as Alpha.
    
    alpha = image.convert("L")
    
    # Create final image
    final_img = Image.new("RGBA", (width, height), text_color)
    final_img.putalpha(alpha)
    
    return final_img

if __name__ == "__main__":
    # Self test
    font_path = r"c:\Quran\fonts\UthmanTNB_v2-0.ttf"
    if load_private_font(font_path):
        print("Font loaded")
        text = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
        img = render_text_to_image(text, "Uthman TNB v2", 100, 800, 300)
        img.save("test_gdi.png")
        print("Saved test_gdi.png")
    else:
        print("Failed load font")
