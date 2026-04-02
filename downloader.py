import json
import os
import requests
import re
from urllib.parse import urlparse

# Paths
API_DUMP_PATH = 'aa/api_dump.json'
BASE_DIR = 'aa/assets'
VID_DIR = f'{BASE_DIR}/videos'
IMG_DIR = f'{BASE_DIR}/images'

# Ensure directories exist
os.makedirs(VID_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

def sanitize_filename(name):
    """Refines a string to be a safe filename across Windows and Unix."""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip().replace(' ', '_')

def download_file(url, target_path):
    """Downloads a file given its URL and a target path."""
    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"FAILED TO DOWNLOAD {url}: {e}")
        return False

# Load data
with open(API_DUMP_PATH, 'r') as f:
    data = json.load(f)

prompts = data.get('prompts', [])
print(f"Found {len(prompts)} prompts to process...")

# Pattern to find media URLs in prompt text
media_pattern = re.findall(r'https?://[^\s\"\']+\.(?:mp4|webm|m3u8|png|jpg|jpeg|webp|gif)', json.dumps(data))
# (Wait, regex on the whole JSON might miss the title connection)

# Let's iterate by prompt for better naming
for i, p in enumerate(prompts):
    title = p.get('title', f"prompt_{i}")
    safe_title = sanitize_filename(title)
    text = p.get('prompt_text', '')
    
    # Extract all media URLs from this prompt's text
    urls = re.findall(r'https?://[^\s\"\']+\.(?:mp4|webm|m3u8|png|jpg|jpeg|webp|gif)', text)
    
    # Also check if there's a specific 'image_url' or other fields (if any exist)
    for key, val in p.items():
        if isinstance(val, str) and 'http' in val and any(ext in val.lower() for ext in ['.mp4', '.webm', '.m3u8', '.png', '.jpg', '.jpeg', '.webp', '.gif']):
            if val not in urls:
                urls.append(val)

    if not urls:
        print(f"[{i+1}/{len(prompts)}] No assets found for '{title}'")
        continue

    print(f"[{i+1}/{len(prompts)}] Processing '{title}' with {len(urls)} assets...")

    for j, url in enumerate(urls):
        ext = os.path.splitext(urlparse(url).path)[1]
        if not ext: 
            # Fallback if extension is not in the path (e.g., query params)
            if 'mp4' in url.lower(): ext = '.mp4'
            elif 'webm' in url.lower(): ext = '.webm'
            elif 'png' in url.lower(): ext = '.png'
            elif 'jpg' in url or 'jpeg' in url: ext = '.jpg'
            elif 'webp' in url.lower(): ext = '.webp'
            elif 'm3u8' in url.lower(): ext = '.mp4' # Treat HLS as mp4 if we had a converter, but for now just label it
            else: ext = '.dat'

        # Target naming
        suffix = f"_{j}" if len(urls) > 1 else ""
        folder = VID_DIR if ext.lower() in ['.mp4', '.webm', '.m3u8'] else IMG_DIR
        filename = f"{safe_title}{suffix}{ext}"
        target_path = os.path.join(folder, filename)

        if os.path.exists(target_path):
            print(f"  - Already exists: {filename}")
            continue

        print(f"  - Downloading {filename}...")
        download_file(url, target_path)

print("\n--- DOWNLOAD PROCESS COMPLETE ---")
