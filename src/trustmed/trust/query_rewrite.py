"""Query rewriting: turn plain language into medical search terms."""
from ..rag.llm import LLM

REWRITE_PROMPT = """You turn questions about breast cancer into a short search query
for a database of medical research papers.
- Use precise medical terms, e.g. "chemo" -> "chemotherapy", "cold cap" -> "scalp cooling",
  "hair loss" -> "alopecia", "drug that blocks oestrogen" -> "endocrine therapy / tamoxifen".
- Keep the original meaning. Do not add new topics, drugs or claims.
- Reply with ONLY the rewritten query on one line. No explanation."""


class QueryRewriter:
    def __init__(self):
        self.llm = LLM(model="openai/gpt-oss-20b")   # small and fast is enough

    def rewrite(self, question):
        out = self.llm.generate(
            [{"role": "system", "content": REWRITE_PROMPT},
             {"role": "user", "content": question}],
            temperature=0, max_tokens=512)
        out = (out or "").strip().strip('"')
        return out or question          # if anything goes wrong, we will use the original