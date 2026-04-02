from notte_sdk import NotteClient
import json

client = NotteClient(api_key="sk-notte-135117db202719e7f946773e64eb7d16a8255d764314413f452431fe70be897d")
function = client.Function("844159da-2cb3-4ed2-a3ee-adb26b35ef42")

print("Checking for image URLs...")
res = function.run(fetch_all_texts=True)

if hasattr(res, 'result'):
    prompts = res.result.get("prompts", [])
    if prompts:
        print("Detailed keys for first prompt:")
        first_prompt = prompts[0]
        # Printing all keys
        for key, value in first_prompt.items():
            if isinstance(value, str) and value.startswith('http'):
                print(f"URL found in '{key}': {value}")
            else:
                print(f"Key: '{key}' | Value type: {type(value)}")
        
        # Printing the full dict just in case
        print("\nFull dict of first prompt:")
        print(json.dumps(first_prompt, indent=2))
    else:
        print("No prompts found.")
else:
    print("No result found.")
