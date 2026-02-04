import ctypes
from ctypes import wintypes

# GDI Constants
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20

gdi32 = ctypes.windll.gdi32
user32 = ctypes.windll.user32

# Define LOGFONTW manually as it's missing in some python wintypes
class LOGFONTW(ctypes.Structure):
    _fields_ = [
        ("lfHeight", wintypes.LONG),
        ("lfWidth", wintypes.LONG),
        ("lfEscapement", wintypes.LONG),
        ("lfOrientation", wintypes.LONG),
        ("lfWeight", wintypes.LONG),
        ("lfItalic", wintypes.BYTE),
        ("lfUnderline", wintypes.BYTE),
        ("lfStrikeOut", wintypes.BYTE),
        ("lfCharSet", wintypes.BYTE),
        ("lfOutPrecision", wintypes.BYTE),
        ("lfClipPrecision", wintypes.BYTE),
        ("lfQuality", wintypes.BYTE),
        ("lfPitchAndFamily", wintypes.BYTE),
        ("lfFaceName", wintypes.WCHAR * 32)
    ]

class TEXTMETRICW(ctypes.Structure):
    _fields_ = [
        ("tmHeight", wintypes.LONG),
        ("tmAscent", wintypes.LONG),
        ("tmDescent", wintypes.LONG),
        ("tmInternalLeading", wintypes.LONG),
        ("tmExternalLeading", wintypes.LONG),
        ("tmAveCharWidth", wintypes.LONG),
        ("tmMaxCharWidth", wintypes.LONG),
        ("tmWeight", wintypes.LONG),
        ("tmOverhang", wintypes.LONG),
        ("tmDigitizedAspectX", wintypes.LONG),
        ("tmDigitizedAspectY", wintypes.LONG),
        ("tmFirstChar", wintypes.WCHAR),
        ("tmLastChar", wintypes.WCHAR),
        ("tmDefaultChar", wintypes.WCHAR),
        ("tmBreakChar", wintypes.WCHAR),
        ("tmItalic", wintypes.BYTE),
        ("tmUnderlined", wintypes.BYTE),
        ("tmStruckOut", wintypes.BYTE),
        ("tmPitchAndFamily", wintypes.BYTE),
        ("tmCharSet", wintypes.BYTE)
    ]

# Font Enum Callback
FONTENUMPROC = ctypes.WINFUNCTYPE(
    ctypes.c_int,
    ctypes.POINTER(LOGFONTW),
    ctypes.POINTER(TEXTMETRICW),
    wintypes.DWORD,
    wintypes.LPARAM
)

def enum_font_fam_proc(lpelf, lpntm, FontType, lParam):
    lf = lpelf.contents
    print(f"Font Found: {lf.lfFaceName}")
    print(f"  > LF CharSet: {lf.lfCharSet}")
    return 1

def check_font_name():
    font_path = r"c:\Quran\fonts\UthmanTNB_v2-0.ttf"
    
    # 1. Load Font
    ret = gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
    print(f"AddFontResourceEx result: {ret}")
    
    if ret == 0:
        print("Failed to load font file!")
        return

    # 2. Enumerate Fonts to match
    hwin = user32.GetDesktopWindow()
    hdc = user32.GetDC(hwin)
    
    callback = FONTENUMPROC(enum_font_fam_proc)
    
    print("\nEnumerating fonts matching 'Uthman'...")
    # EnumFontFamiliesW(hdc, lpszFamily, lpEnumFontFamProc, lParam)
    # Pass None to list all, or partial string if possible (GDI usually exact match or null)
    # We'll list ALL and filter in python to find our font
    
    gdi32.EnumFontFamiliesW(hdc, None, callback, 0)
    
    # Clean up
    gdi32.RemoveFontResourceExW(font_path, FR_PRIVATE, 0)
    user32.ReleaseDC(hwin, hdc)

if __name__ == "__main__":
    check_font_name()
