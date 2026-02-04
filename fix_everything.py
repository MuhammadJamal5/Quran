import requests
import os
import shutil

# List of potential mirrors
MIRRORS = [
    "https://raw.githubusercontent.com/cchartm16/quran/master/quran-uthmani.txt",
    "https://raw.githubusercontent.com/semarch/quran/master/tanzil/quran-uthmani.txt",
    "https://raw.githubusercontent.com/GlobalQuran/quran-data/master/quran-uthmani.txt",
    "https://raw.githubusercontent.com/mohammed-mostafa/quran-data/master/tanzil/quran-uthmani.txt",
    "https://raw.githubusercontent.com/khalidalhobaya/quran-data/master/quran-uthmani.txt"
]

TEXT_PATH = r"c:\Quran\quran_text\quran-uthmani.txt"
FONT_PATH = r"c:\Quran\fonts\Amiri-Quran.ttf"

def fix_system():
    print("=== STARTING FINAL FIX ===")
    
    # --- Step 1: Download Text ---
    print("\n[1/3] Downloading Full Quran Text...")
    downloaded = False
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for url in MIRRORS:
        print(f"Trying: {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                content = response.text
                if "1|1|" in content[:500] and len(content) > 500000:
                    with open(TEXT_PATH, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"SUCCESS: Downloaded {len(content)} bytes.")
                    downloaded = True
                    break
                else:
                    print(f"FAILED: Invalid content (First 50 chars: {content[:50]!r})")
            else:
                print(f"FAILED: HTTP {response.status_code}")
        except Exception as e:
            print(f"FAILED: Error {e}")
            
    if not downloaded:
        print("CRITICAL ERROR: All mirrors failed.")

    # --- Step 2: Verify Font ---
    print("\n[2/3] Verifying Font...")
    if os.path.exists(FONT_PATH) and os.path.getsize(FONT_PATH) > 100000:
        print(f"SUCCESS: Amiri-Quran.ttf found ({os.path.getsize(FONT_PATH)} bytes).")
    else:
        print("ERROR: Font missing or empty.")

    # --- Step 3: Summary ---
    print("\n[3/3] System Status")
    if os.path.exists(TEXT_PATH) and os.path.getsize(TEXT_PATH) > 500000:
        print(">> READY TO RUN.")
        print(">> Please RESTART 'Run QuranReelMaker.bat'")
    else:
        print(">> STILL BROKEN: Text file missing.")

if __name__ == "__main__":
    fix_system()
