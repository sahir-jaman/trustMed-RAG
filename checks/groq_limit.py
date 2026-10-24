import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"), max_retries=0)

for model in ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]:
    print("=" * 70)
    print(model)
    try:
        raw = client.chat.completions.with_raw_response.create(
            model=model, messages=[{"role": "user", "content": "hi"}], max_completion_tokens=5)
        h = raw.headers
        print("✅ Available now")
        print("  requests left today :", h.get("x-ratelimit-remaining-requests"),
              "| resets in", h.get("x-ratelimit-reset-requests"))
        print("  tokens left (minute):", h.get("x-ratelimit-remaining-tokens"),
              "| resets in", h.get("x-ratelimit-reset-tokens"))
    except Exception as e:
        print("❌ Blocked:")
        print(" ", e)