import requests
import os

# Reliable GitHub mirror for Tanzil Uthmani text
# List of potential mirrors
MIRRORS = [
    "https://raw.githubusercontent.com/nuqayah/quran-text/master/data/quran-uthmani.txt",
    "https://raw.githubusercontent.com/nuqayah/quran-text/main/data/quran-uthmani.txt",
    "https://raw.githubusercontent.com/khalidalhobaya/quran-data/master/quran-uthmani.txt",
    "https://raw.githubusercontent.com/islamic-network/quran-text/master/quran-uthmani.txt",
    "https://raw.githubusercontent.com/semarch/quran/master/tanzil/quran-uthmani.txt"
]

DEST_DIR = r"c:\Quran\quran_text"
DEST_FILE = os.path.join(DEST_DIR, "quran-uthmani.txt")

def download_text():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    for url in MIRRORS:
        print(f"Trying mirror: {url} ...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # Validate content
                if "1|1|" in response.text[:500]:
                    with open(DEST_FILE, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"SUCCESS: Full Quran saved from {url}")
                    print(f"Size: {os.path.getsize(DEST_FILE)} bytes")
                    return True
                else:
                    print(f"  -> Invalid content (not Tanzil format)")
            else:
                print(f"  -> Failed (Status {response.status_code})")
        except Exception as e:
            print(f"  -> Error: {e}")
            
    print("ALL MIRRORS FAILED.")
    return False

if __name__ == "__main__":
    download_text()
