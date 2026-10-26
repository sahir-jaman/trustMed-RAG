"""Streamlit frontend for TrustMed.
Start the API first, then run:  streamlit run src/app/ui.py"""
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/chat"     # must match your FastAPI route

ICON = {"supported": "✅", "partial": "🟡", "unsupported": "⚠️",
        "no_citation": "⚠️", "unknown": "❓", "skip": ""}

EXAMPLES = [
    "Does trastuzumab improve survival in HER2-positive breast cancer?",               # normal answer
    "Is albumin-bound paclitaxel more effective than docetaxel?",                      # retraction warning
    "Does a cold cap stop hair falling out from chemo?",                               # query rewriting
    "I have breast cancer. Should I stop taking tamoxifen because of hot flashes?",    # safety refusal
    "What is the best treatment for lung cancer?",                                     # not enough evidence
    "Can scalp cooling prevent hair loss during chemotherapy?",                        # claim checking
]

st.set_page_config(page_title="TrustMed", page_icon="🩺", layout="centered")
st.markdown("""
<style>
html { font-size: 17px; }                       /* all text a little bigger */
p, li { line-height: 1.7; }                     /* more comfortable reading */
.stTextInput input { font-size: 1.05rem; padding: 0.7rem 0.9rem; }   /* bigger question box */
.stButton button { border-radius: 999px; }      /* rounded buttons */
</style>
""", unsafe_allow_html=True)

st.title("🩺 TrustMed")
st.caption("Answers from 5,000+ breast cancer research papers, with retraction checks, "
           "evidence badges and sentence-by-sentence claim checking.")

# --- Example questions (clicking one fills the question box) ---
if "question" not in st.session_state:
    st.session_state.question = ""

st.write("**Try an example:**")
cols = st.columns(2)
for i, example in enumerate(EXAMPLES):
    if cols[i % 2].button(example, use_container_width=True):
        st.session_state.question = example

question = st.text_input("Your question", key="question",
                         placeholder="e.g. Does exercise reduce fatigue in breast cancer survivors?")

# --- Ask the API ---
if st.button("Submit", type="primary") and question.strip():
    with st.spinner("Searching papers and checking every claim… (10–30 seconds)"):
        try:
            r = requests.post(API_URL, json={"question": question}, timeout=180)
        except requests.ConnectionError:
            st.error("Can't reach the TrustMed API. Is it running?  "
                     "(uvicorn app.api:app --app-dir src)")
            st.stop()

    if r.status_code != 200:
        try:
            st.error(r.json().get("detail", "Something went wrong."))
        except ValueError:
            st.error("Something went wrong.")
        st.stop()

    result = r.json()

    # Warnings first, so they're impossible to miss
    for w in result["warnings"]:
        st.warning(w)

    # The answer, sentence by sentence
    st.subheader("Answer")
    if result["claims"]:
        for c in result["claims"]:
            st.markdown(f"{ICON.get(c['status'], '')} {c['sentence']}")
        st.caption("✅ supported by the cited source · 🟡 partly supported · ⚠️ not supported or no citation")
    else:
        st.write(result["answer"])       # refusals / "not enough evidence"

    if result.get("search_query"):
        st.caption(f"🔎 Searched for: *{result['search_query']}*")

    # Source cards
    if result["sources"]:
        st.subheader("Sources")
        for s in result["sources"]:
            with st.container(border=True):
                st.markdown(f"**[{s['n']}] [{s['title']}]({s['url']})**")
                st.caption(f"{s['badge']} evidence · {s['journal']} · {s['year']} · section: {s['section']}")
                with st.expander("Show the passage used"):
                    st.write(s.get("text", ""))

    st.info(result["disclaimer"])