"""
Smart Study Assistant
----------------------
Paste in notes or article text and:
  1. Get a concise summary
  2. Sit an auto-generated exam with instant right/wrong feedback
  3. Ask follow-up questions about the material

Powered by the Gemini API (free tier). API key is read only from a local
.env file — nothing is ever typed or shown on screen.
"""

import os
from typing import List, Optional

import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai

load_dotenv()

MODEL = "gemini-3.6-flash"  # free-tier friendly, fast model

st.set_page_config(
    page_title="Smart Study Assistant",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Design system
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    color-scheme: light;
    --bg: #faf8f3;
    --surface: #ffffff;
    --surface-2: #f3f0e7;
    --border: #e4e0d6;
    --accent: #b87d2b;
    --accent-soft: #8f5e1c;
    --accent-tint: #f1e2c9;
    --success: #1b8a5a;
    --success-bg: #e7f5ee;
    --error: #c0392b;
    --error-bg: #fbeae8;
    --text: #201d18;
    --text-muted: #6b6860;
}

html, body {
    color-scheme: light;
}

#MainMenu, footer, header, [data-testid="collapsedControl"] { visibility: hidden; height: 0; }

.stApp {
    background: radial-gradient(ellipse 900px 420px at 50% -10%, rgba(184,125,43,0.10), transparent 60%), var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container { padding-top: 3rem; max-width: 760px; }

.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-soft);
    font-size: 0.72rem;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.5rem;
    line-height: 1.12;
    margin: 0 0 0.6rem 0;
    color: var(--text);
}
.hero-sub { color: var(--text-muted); font-size: 1rem; margin-bottom: 1.8rem; }

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 2.2rem 0 0.7rem 0;
}

.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

.stButton button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.55rem 1rem !important;
    transition: border-color 0.15s ease, transform 0.1s ease;
}
.stButton button:hover { border-color: var(--accent) !important; color: var(--accent-soft) !important; }
.stButton button:active { transform: scale(0.98); }
.stButton button:focus-visible { outline: 2px solid var(--accent) !important; outline-offset: 2px; }

.stButton button[kind="primary"] {
    background: var(--accent) !important;
    color: #fffaf0 !important;
    border: none !important;
    font-weight: 600 !important;
}
.stButton button[kind="primary"]:hover { background: var(--accent-soft) !important; color: #fffaf0 !important; }

[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

.quiz-q-num {
    font-family: 'JetBrains Mono', monospace;
    color: var(--accent-soft);
    font-size: 0.76rem;
    letter-spacing: 0.08em;
}
.quiz-question { font-family: 'Fraunces', serif; font-size: 1.12rem; font-weight: 600; margin: 0.35rem 0 1rem 0; }
.quiz-option { display: block; width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 0.5rem; font-size: 0.92rem; }
.quiz-option.correct { background: var(--success-bg); border-color: var(--success); color: var(--success); font-weight: 600; }
.quiz-option.incorrect { background: var(--error-bg); border-color: var(--error); color: var(--error); font-weight: 600; }
.quiz-option.neutral { color: var(--text-muted); }
.quiz-explanation { font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px dashed var(--border); }

.score-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    background: var(--accent-tint);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.32rem 0.9rem;
    font-size: 0.82rem;
    color: var(--accent-soft);
}

.footer-note { text-align: center; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; margin-top: 3rem; opacity: 0.7; }

@media (max-width: 640px) { .hero-title { font-size: 1.9rem; } }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# API key — read silently from .env, nothing shown on screen
# ---------------------------------------------------------------------------
ENV_KEY = os.environ.get("GEMINI_API_KEY")


def get_client() -> genai.Client:
    return genai.Client(api_key=ENV_KEY)


# ---------------------------------------------------------------------------
# Structured output schema for the exam
# ---------------------------------------------------------------------------
class QuizQuestion(BaseModel):
    question: str = Field(description="The quiz question text.")
    options: List[str] = Field(description="Exactly 4 answer options, in order.")
    correct_index: int = Field(description="Index (0-3) of the correct option.")
    explanation: str = Field(description="One sentence explaining why the correct answer is right.")


class QuizSet(BaseModel):
    questions: List[QuizQuestion] = Field(description="5 multiple-choice questions.")


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
st.session_state.setdefault("notes", "")
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("quiz", None)
st.session_state.setdefault("quiz_selected", {})

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="hero-eyebrow">AI Study Tools · Gemini</div>
<div class="hero-title">📚 Smart Study Assistant</div>
<div class="hero-sub">Paste your notes, get a summary, sit an exam on the material, or ask follow-up questions.</div>
""",
    unsafe_allow_html=True,
)

if not ENV_KEY:
    with st.container(border=True):
        st.markdown(
            f'<span style="color: var(--error); font-weight: 600;">No API key found</span>',
            unsafe_allow_html=True,
        )
        st.write(
            "Add `GEMINI_API_KEY=your_key` to a `.env` file in this project folder, "
            "then restart the app. Get a free key at "
            "[aistudio.google.com/apikey](https://aistudio.google.com/apikey)."
        )
    st.stop()

# ---------------------------------------------------------------------------
# Notes input
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Your notes</div>', unsafe_allow_html=True)
notes = st.text_area(
    "notes",
    height=220,
    value=st.session_state.notes,
    placeholder="Paste your notes or article here...",
    label_visibility="collapsed",
)
st.session_state.notes = notes

col1, col2 = st.columns(2)
with col1:
    summarize_clicked = st.button("📝 Summarize", use_container_width=True, type="primary")
with col2:
    quiz_clicked = st.button("🎓 Start Exam", use_container_width=True, type="primary")

if summarize_clicked:
    if not notes.strip():
        st.warning("Paste some text first.")
    else:
        client = get_client()
        with st.spinner("Summarizing..."):
            interaction = client.interactions.create(
                model=MODEL,
                input=(
                    "Summarize the following notes in 4-6 concise bullet points, "
                    f"focused on the key ideas:\n\n{notes}"
                ),
            )
        st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(interaction.output_text)

if quiz_clicked:
    if not notes.strip():
        st.warning("Paste some text first.")
    else:
        client = get_client()
        with st.spinner("Writing your exam..."):
            interaction = client.interactions.create(
                model=MODEL,
                input=(
                    "Create a 5-question multiple-choice quiz that tests understanding "
                    "of the following notes. Each question must have exactly 4 options "
                    "with only one correct answer, plus a one-sentence explanation of "
                    f"why that answer is correct.\n\n{notes}"
                ),
                response_format={
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": QuizSet.model_json_schema(),
                },
            )
        quiz_set = QuizSet.model_validate_json(interaction.output_text)
        st.session_state.quiz = [q.model_dump() for q in quiz_set.questions]
        st.session_state.quiz_selected = {}

# ---------------------------------------------------------------------------
# Exam mode
# ---------------------------------------------------------------------------
quiz = st.session_state.quiz
if quiz:
    st.markdown('<div class="section-label">Exam mode</div>', unsafe_allow_html=True)

    answered = st.session_state.quiz_selected
    correct_count = sum(1 for i, sel in answered.items() if sel == quiz[i]["correct_index"])
    st.markdown(
        f'<span class="score-badge">Score: {correct_count} correct · '
        f'{len(answered)} / {len(quiz)} answered</span>',
        unsafe_allow_html=True,
    )
    st.write("")

    for i, q in enumerate(quiz):
        with st.container(border=True):
            st.markdown(f'<div class="quiz-q-num">QUESTION {i + 1} OF {len(quiz)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="quiz-question">{q["question"]}</div>', unsafe_allow_html=True)

            selected: Optional[int] = answered.get(i)

            if selected is None:
                for j, opt in enumerate(q["options"]):
                    if st.button(opt, key=f"q{i}_opt{j}", use_container_width=True):
                        st.session_state.quiz_selected[i] = j
                        st.rerun()
            else:
                for j, opt in enumerate(q["options"]):
                    if j == q["correct_index"]:
                        css_class, prefix = "correct", "✓ "
                    elif j == selected:
                        css_class, prefix = "incorrect", "✕ "
                    else:
                        css_class, prefix = "neutral", ""
                    st.markdown(f'<div class="quiz-option {css_class}">{prefix}{opt}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="quiz-explanation">{q["explanation"]}</div>', unsafe_allow_html=True)

    if st.button("🔄 New exam from these notes"):
        st.session_state.quiz = None
        st.session_state.quiz_selected = {}
        st.rerun()

# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Ask about your notes</div>', unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask something about the text above...")
if question:
    if not notes.strip():
        st.warning("Paste your notes above first so there's context to answer from.")
    else:
        client = get_client()
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                prompt = (
                    f"Here are some notes:\n\n{notes}\n\n"
                    "Answer the question below using only the notes above. "
                    "If the answer isn't in the notes, say so clearly.\n\n"
                    f"Question: {question}"
                )
                interaction = client.interactions.create(model=MODEL, input=prompt)
                answer = interaction.output_text
                st.write(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})

if st.session_state.chat_history:
    if st.button("🗑️ Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown('<div class="footer-note">Built with Streamlit + Gemini</div>', unsafe_allow_html=True)
