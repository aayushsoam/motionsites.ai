import csv
from notte_sdk import NotteClient

client = NotteClient(api_key="sk-notte-135117db202719e7f946773e64eb7d16a8255d764314413f452431fe70be897d")
function = client.Function("844159da-2cb3-4ed2-a3ee-adb26b35ef42")

res = function.run(fetch_all_texts=True)

prompts = res.result["prompts"]
errors  = res.result.get("errors", [])

with open("motionsites_prompts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "title", "category", "type", "is_free", "prompt_text"])
    writer.writeheader()
    for p in prompts:
        writer.writerow(p)

print(f"Fetched: {len(prompts)} prompts")
print(f"Skipped (premium): {len(errors)}")
print("Saved: motionsites_prompts.csv")