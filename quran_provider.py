import os

# Path to the single source of truth
QURAN_FILE = os.path.join(os.path.dirname(__file__), 'quran_text', 'quran-uthmani.txt')

# Cache: { (sura, ayah): text }
_QURAN_CACHE = {}
# Cache: { sura: { ayah: text } } for faster full surah access
_SURAH_CACHE = {}

def load_quran():
    """Parses quran-uthmani.txt into memory."""
    global _QURAN_CACHE, _SURAH_CACHE
    if _QURAN_CACHE:
        return

    if not os.path.exists(QURAN_FILE):
        # Fallback check for simple text just to give a better error, or mistakenly renamed file
        return

    try:
        count = 0
        with open(QURAN_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split('|')
                if len(parts) >= 3:
                    try:
                        sura = int(parts[0])
                        ayah = int(parts[1])
                        text = parts[2]
                        
                        # Store in flat cache
                        _QURAN_CACHE[(sura, ayah)] = text
                        
                        # Store in surah cache
                        if sura not in _SURAH_CACHE:
                            _SURAH_CACHE[sura] = {}
                        _SURAH_CACHE[sura][ayah] = text
                        
                        count += 1
                    except ValueError:
                        continue
        print(f"[INFO] Loaded {count} ayahs from quran-uthmani.txt")

    except Exception as e:
        print(f"[ERROR] Failed to load Quran file: {e}")

def get_ayah_text(sura, ayah):
    """Returns single ayah text."""
    if not _QURAN_CACHE:
        load_quran()
    return _QURAN_CACHE.get((sura, ayah))

def get_surah(sura):
    """
    Returns a list of all ayah texts for a given surah, in order.
    Returns [] if surah not found.
    """
    if not _QURAN_CACHE:
        load_quran()
        
    if sura not in _SURAH_CACHE:
        return []
        
    # Sort by ayah number to ensure order
    ayahs = _SURAH_CACHE[sura]
    return [ayahs[k] for k in sorted(ayahs.keys())]

def get_range(sura, start, end):
    """
    Returns a list of ayah texts for the range [start, end] inclusive.
    """
    if not _QURAN_CACHE:
        load_quran()
        
    texts = []
    for i in range(start, end + 1):
        t = _QURAN_CACHE.get((sura, i))
        if t:
            texts.append(t)
    return texts

def is_source_available():
    return os.path.exists(QURAN_FILE)
