import os
import glob
import re

PROMPTS_DIR = "prompts"
VIDEOS_DIR = "assets/videos"

def update_prompt_file(filepath):
    """Updates a single prompt markdown file with local video previews."""
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    
    # Standardize name for matching (some files might have hyphens/underscores)
    # But based on list_dir, names match exactly (e.g. AI_Designer_Agency.md and AI_Designer_Agency_0.mp4)
    
    # Find all matching videos
    pattern = os.path.join(VIDEOS_DIR, f"{base_name}_*")
    matching_videos = [v for v in glob.glob(pattern) if v.endswith(('.mp4', '.webm'))]
    
    if not matching_videos:
        print(f"  [SKIP] No videos found for {base_name}")
        return False
    
    # Sort them numerically if possible (Prompt_0, Prompt_1, etc.)
    matching_videos.sort()
    
    print(f"  [UPDATE] Found {len(matching_videos)} videos for {base_name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Construct the new video section
    # GitHub renders ![caption](path.mp4) as a video player
    video_section = "## 🎬 Video Preview\n\n"
    for i, video in enumerate(matching_videos):
        rel_path = os.path.join("..", video).replace("\\", "/")
        video_section += f"![Video Preview {i}]({rel_path})\n\n"
    
    # Regex to find the current Video Preview section and replace it
    # It usually starts with ## 🎬 Video Preview and ends before the next ## section (usually ## 📋 Prompt)
    # The pattern matches across multiple lines (DOTALL)
    # We look for the start and then match everything until the next '## ' or end of string.
    pattern_regex = r"## 🎬 Video Preview.*?(?=\n## |$)"
    
    if re.search(pattern_regex, content, flags=re.DOTALL):
        new_content = re.sub(pattern_regex, video_section.strip(), content, flags=re.DOTALL)
    else:
        # If not found, insert after the first H1 or at the top
        print(f"  [INSERT] Video section not found, inserting at top of {base_name}")
        if content.startswith("#"):
            lines = content.splitlines()
            # Find the first empty line after the title
            inserted = False
            for idx, line in enumerate(lines):
                if idx > 0 and line.strip() == "":
                    lines.insert(idx + 1, "---\n\n" + video_section)
                    inserted = True
                    break
            if not inserted:
                lines.insert(1, "\n" + video_section)
            new_content = "\n".join(lines)
        else:
            new_content = video_section + "---\n\n" + content
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    if not os.path.exists(PROMPTS_DIR):
        print(f"Error: {PROMPTS_DIR} directory not found.")
        return

    prompt_files = glob.glob(os.path.join(PROMPTS_DIR, "*.md"))
    print(f"Syncing {len(prompt_files)} prompt files...")
    
    updated_count = 0
    for pf in prompt_files:
        if update_prompt_file(pf):
            updated_count += 1
            
    print(f"\nDone! Updated {updated_count} files.")

if __name__ == "__main__":
    main()
