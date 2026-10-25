"""Safety layer: spot personal medical-advice questions before answering."""
from ..rag.llm import LLM

DISCLAIMER = ("TrustMed summarises published research for educational purposes. "
              "It is not medical advice. Always talk to your doctor about your own care.")

REFUSAL = ("I can't give personal medical advice, such as whether to start, stop or change a treatment. "
           "Please talk to your doctor or care team, who know your situation. "
           "You can ask me a general research question instead, for example: "
           "\"What does research say about managing hot flashes during tamoxifen treatment?\"")

CLASSIFIER_PROMPT = """You check questions sent to a breast cancer research assistant.
Reply with exactly one word:
PERSONAL - the person asks what THEY (or a specific person they know) should do about their own health,
           symptoms, diagnosis or treatment. These usually mention "I", "my", "me", or a specific
           person ("my mum", "my sister", "she").
RESEARCH - a general question about what research shows, even if written in everyday words.

Examples:
"Should I stop my chemo?" -> PERSONAL
"My mum has HER2-positive cancer. Which drug should she take?" -> PERSONAL
"I found a lump, is it cancer?" -> PERSONAL
"Does tamoxifen cause hot flashes?" -> RESEARCH
"I read about trastuzumab. How well does it work?" -> RESEARCH
"Do anti-sickness pills help with chemo nausea?" -> RESEARCH
"Does losing weight lower the chance of cancer coming back?" -> RESEARCH"""


class SafetyChecker:
    def __init__(self):
        self.llm = LLM(model="openai/gpt-oss-20b")   # small and fast is enough for this

    def is_personal_advice(self, question):
        reply = self.llm.generate(
            [{"role": "system", "content": CLASSIFIER_PROMPT},
             {"role": "user", "content": question}],
            temperature=0, max_tokens=512)
        return "PERSONAL" in (reply or "").upper()