from notte_sdk import NotteClient

client = NotteClient(api_key="sk-notte-135117db202719e7f946773e64eb7d16a8255d764314413f452431fe70be897d")
function = client.Function("844159da-2cb3-4ed2-a3ee-adb26b35ef42")

res = function.run(prompt_id="bloom-ai-hero")

print(res.result["prompt_text"])