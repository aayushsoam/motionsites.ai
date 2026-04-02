from notte_sdk import NotteClient
import csv
import json

client = NotteClient(api_key="sk-notte-135117db202719e7f946773e64eb7d16a8255d764314413f452431fe70be897d")
function = client.Function("844159da-2cb3-4ed2-a3ee-adb26b35ef42")

print("Fetching all prompts and their texts...")
res = function.run(fetch_all_texts=True)

prompts = res.result.get("prompts", [])
# Some prompts might be in 'errors' if they are protected/premium but we have fetch_all_texts=True.
errors = res.result.get("errors", [])

print(f"Retrieved {len(prompts)} prompts.")
if errors:
    print(f"Note: {len(errors)} items had errors or were restricted.")

# Prepare CSV output
filename = "all_motionsites_prompts.csv"
fieldnames = ["id", "title", "category", "type", "is_free", "prompt_text"]

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for p in prompts:
        # Map fields, handle missing ones
        row = {
            "id": p.get("id", ""),
            "title": p.get("title", ""),
            "category": p.get("category", ""),
            "type": p.get("type", ""),
            "is_free": p.get("is_free", ""),
            "prompt_text": p.get("prompt_text", "")
        }
        writer.writerow(row)

print(f"Successfully saved to {filename}")
