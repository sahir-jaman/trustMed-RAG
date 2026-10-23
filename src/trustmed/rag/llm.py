"""Sends messages to the LLM. Only this file knows which provider we use."""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
DEFAULT_MODEL = "openai/gpt-oss-120b"


class LLM:
    def __init__(self, model=DEFAULT_MODEL):
        self.model = model
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, messages, temperature=0.1, max_tokens=2048):
        reply = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,        # low = factual and consistent
            max_completion_tokens=max_tokens,
            reasoning_effort="low",         # gpt-oss "thinks" first; low keeps it fast
        )
        return reply.choices[0].message.content