"""Builds the prompt sent to the LLM."""

SYSTEM_PROMPT = """You are TrustMed, a research assistant that summarises breast cancer research.

Rules:
1. Answer ONLY using the numbered sources provided. Do not use outside knowledge.
2. After every factual sentence, cite the source(s) it comes from, like [1] or [2][3].
3. If the sources do not contain enough information to answer, say:
   "The provided research does not contain enough evidence to answer this question."
4. Be concise: at most 5 sentences.
5. Write for an educated non-specialist. Explain medical terms briefly.
6. Use ONLY plain square-bracket citations like [1] or [2][3]. No other citation format.
"""


def format_sources(chunks):
    """Turn retrieved chunks into a numbered list the model can cite."""
    parts = []
    for i, c in enumerate(chunks, start=1):
        parts.append(
            f"[{i}] {c['title']} ({c['journal']}, {c['year']}) "
            f"| {c['study_type']} | section: {c['section']}\n{c['text']}"
        )
    return "\n\n".join(parts)


def build_messages(question, chunks):
    """Return the messages list for the chat API."""
    user_message = f"Sources:\n\n{format_sources(chunks)}\n\nQuestion: {question}"
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]