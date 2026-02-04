# Quick Test Script
# Test if the Quran Reels Generator is working correctly

import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("\n" + "="*60)
print("  Quran Cinematic Reels Generator - Quick Test")
print("="*60 + "\n")

# Test 1: Check if server is running
print("[1/4] Testing server connection...")
try:
    response = requests.get(BASE_URL, timeout=5)
    if response.status_code == 200:
        print("   ✓ Server is running")
    else:
        print(f"   ✗ Server returned status {response.status_code}")
        exit(1)
except Exception as e:
    print(f"   ✗ Cannot connect to server: {e}")
    print("   Please start the server first: python main.py")
    exit(1)

# Test 2: Test video generation with short ayah
print("\n[2/4] Testing video generation (Surah 108, Ayah 1)...")
print("   This will take ~30-45 seconds...")

test_data = {
    "reciter": "abdulbasit/murattal",
    "surah": 108,
    "ayah_from": 1,
    "ayah_to": 1
}

try:
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/generate",
        json=test_data,
        timeout=300  # 5 minutes max
    )
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ Video generated successfully in {elapsed:.1f}s")
        print(f"   Video URL: {result.get('video_url')}")
        video_url = result.get('video_url')
    else:
        print(f"   ✗ Generation failed: {response.json().get('error')}")
        exit(1)
except Exception as e:
    print(f"   ✗ Error during generation: {e}")
    exit(1)

# Test 3: Check if video file exists
print("\n[3/4] Checking generated video...")
try:
    video_response = requests.head(BASE_URL + video_url, timeout=5)
    if video_response.status_code == 200:
        size = int(video_response.headers.get('content-length', 0))
        print(f"   ✓ Video file exists ({size / 1024 / 1024:.2f} MB)")
    else:
        print(f"   ✗ Video file not accessible")
        exit(1)
except Exception as e:
    print(f"   ✗ Cannot access video: {e}")
    exit(1)

# Test 4: Verify video is downloadable
print("\n[4/4] Testing video download...")
try:
    download_response = requests.get(BASE_URL + video_url, timeout=30, stream=True)
    if download_response.status_code == 200:
        # Get first chunk to verify
        first_chunk = next(download_response.iter_content(1024))
        if first_chunk:
            print(f"   ✓ Video is downloadable")
        else:
            print(f"   ✗ Video download failed (empty)")
            exit(1)
    else:
        print(f"   ✗ Cannot download video")
        exit(1)
except Exception as e:
    print(f"   ✗ Download error: {e}")
    exit(1)

# Success summary
print("\n" + "="*60)
print("  ✓ All Tests Passed!")
print("="*60)
print("\nYour Quran Cinematic Reels Generator is working perfectly!")
print("\nYou can now:")
print("  1. Open http://localhost:5000 in your browser")
print("  2. Generate beautiful Quran reels")
print("  3. Share them on social media")
print("\n" + "="*60 + "\n")
