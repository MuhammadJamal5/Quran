import requests
import os

URL = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
DEST_DIR = r"c:\Quran\fonts"
DEST_FILE = os.path.join(DEST_DIR, "Amiri-Quran.ttf")

def download_font():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        
    print(f"Downloading Amiri-Quran.ttf from {URL}...")
    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
        
        with open(DEST_FILE, 'wb') as f:
            f.write(response.content)
            
        print(f"SUCCESS: Font saved to {DEST_FILE}")
        print(f"Size: {os.path.getsize(DEST_FILE)} bytes")
        return True
    except Exception as e:
        print(f"ERROR: Download failed: {e}")
        return False

if __name__ == "__main__":
    download_font()
