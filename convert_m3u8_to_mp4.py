import os
import subprocess
import glob
import sys

VIDEO_DIR = os.path.join(os.path.dirname(__file__), "assets", "videos")

def get_url_from_m3u8(filepath):
    """Extract the HLS stream URL from a .m3u8 playlist file."""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("http"):
                return line
    return None

def convert_m3u8_to_mp4(m3u8_path):
    name = os.path.splitext(os.path.basename(m3u8_path))[0]
    out_path = os.path.join(VIDEO_DIR, name + ".mp4")

    # Check if MP4 already exists (skip)
    if os.path.exists(out_path):
        print(f"  [SKIP] MP4 already exists: {name}.mp4")
        return True

    url = get_url_from_m3u8(m3u8_path)
    if not url:
        print(f"  [ERROR] No URL found in {m3u8_path}")
        return False

    print(f"  [DOWNLOADING] {name}")
    print(f"  URL: {url[:80]}...")

    try:
        result = subprocess.run(
            ["yt-dlp", "-f", "best[ext=mp4]/best", "-o", out_path, url],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            print(f"  [OK] Saved: {name}.mp4")
            os.remove(m3u8_path)
            print(f"  [DELETED] {os.path.basename(m3u8_path)}")
            return True
        else:
            print(f"  [FAILED] yt-dlp error:\n{result.stderr[:300]}")
            return False
    except FileNotFoundError:
        print("  [ERROR] yt-dlp not found. Install with: pip install yt-dlp")
        return False
    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] Download took too long for {name}")
        return False

def main():
    m3u8_files = glob.glob(os.path.join(VIDEO_DIR, "*.m3u8"))
    if not m3u8_files:
        print("No .m3u8 files found!")
        return

    print(f"Found {len(m3u8_files)} M3U8 files to convert:\n")

    success = 0
    failed = 0
    for m3u8 in sorted(m3u8_files):
        print(f"\n{'='*50}")
        print(f"Processing: {os.path.basename(m3u8)}")
        if convert_m3u8_to_mp4(m3u8):
            success += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print(f"DONE! Success: {success} | Failed: {failed}")

if __name__ == "__main__":
    main()
