import requests
import os

# Backup Mirror (GitHub)
URL = "https://raw.githubusercontent.com/karim7/quran/master/tanzil/quran-uthmani.txt"
OUTPUT_FILE = "quran-uthmani.txt"

def download_tanzil():
    print(f"Downloading {OUTPUT_FILE} from {URL}...")
    try:
        response = requests.get(URL, stream=True)
        response.raise_for_status()
        
        with open(OUTPUT_FILE, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # Basic Validation
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if "Allah" in content or "God" in content: # Just a sanity check for wrong file, though Uthmani text shouldn't have English
                 # Wait, Uthmani txt usually has no english headers? Or minimal.
                 pass
            
            line_count = len(content.splitlines())
            print(f"Download complete. Lines: {line_count}")
            # Tanzil file usually has metadata lines + 6236 ayahs.
            
    except Exception as e:
        print(f"Failed to download: {e}")

if __name__ == "__main__":
    download_tanzil()
