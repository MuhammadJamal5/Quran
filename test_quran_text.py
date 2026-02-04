import quran_provider
import sys

def test_tanzil_integrity():
    print("Testing Quran Text Integrity (Tanzil Source)...")
    
    # 1. Load Quran
    quran_provider.load_quran()
    
    # 2. Check Count
    count = len(quran_provider._QURAN_CACHE)
    print(f"Loaded Ayahs: {count}/6236")
    
    if count != 6236:
        print("FAIL: Incorrect ayah count!")
        sys.exit(1)
        
    # 3. Verify Specific Ayahs (Uthmani check)
    # Al-Fatiha 1
    fatiha_1 = quran_provider.get_ayah_text(1, 1)
    expected_fatiha = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
    print(f"\n[1:1]\nExpected: {expected_fatiha}\nActual:   {fatiha_1}")
    
    if fatiha_1 != expected_fatiha:
        print("FAIL: Text mismatch in Fatiha:1")
    
    # Al-Ikhlas (112)
    print("\n[112:1-4]")
    ikhlas = quran_provider.get_ayah_text_range(112, 1, 4)
    for i, ayah in enumerate(ikhlas, 1):
        print(f"{i}: {ayah}")
        
    print("\nSUCCESS: Quran text loaded correctly from local file.")

if __name__ == "__main__":
    test_tanzil_integrity()
