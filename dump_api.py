from notte_sdk import NotteClient
import json
import os

client = NotteClient(api_key="sk-notte-135117db202719e7f946773e64eb7d16a8255d764314413f452431fe70be897d")
function = client.Function("844159da-2cb3-4ed2-a3ee-adb26b35ef42")

try:
    res = function.run(fetch_all_texts=True)
    output_path = "c:/Users/thaku/OneDrive/Desktop/my project/browser/aa/api_dump.json"
    
    if hasattr(res, 'result'):
        with open(output_path, "w") as f:
            json.dump(res.result, f, indent=2)
        print(f"Success: Data written to {output_path}")
    else:
        print("Error: 'res' has no 'result' attribute")
except Exception as e:
    print(f"Exception: {str(e)}")
