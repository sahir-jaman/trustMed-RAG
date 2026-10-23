import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()                                   # reads the .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

reply = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "In one sentence, what is HER2-positive breast cancer?"}],
)
print(reply.choices[0].message.content)