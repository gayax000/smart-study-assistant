# 📚 Smart Study Assistant

An AI-powered study tool built with **Streamlit** and the **Gemini API**.

Paste in your notes, an article, or any text, and:
- **Summarize** it into key bullet points
- **Sit an exam** — an auto-generated multiple-choice quiz with instant green/red feedback
- **Ask follow-up questions** about the material in a chat interface

Built as part of a mini project exploring AI tools for coding, research, and productivity.

## Features

- 📝 One-click summarization of long notes/articles
- 🎓 Auto-generated exam mode — pick an answer and see it light up green (correct) or red (incorrect) instantly, with a one-line explanation and a live score badge
- 💬 Chat-based Q&A grounded in your pasted text
- 🔑 API key loaded silently from a local `.env` file — never typed or shown in the UI, never committed to Git

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Gemini API](https://ai.google.dev/) (`google-genai` SDK) — text generation and structured JSON output
- [Pydantic](https://docs.pydantic.dev/) — schema for the exam questions
- Python 3.9+

## Live Demo

[smartstudy-assistant-app.streamlit.app](https://smartstudy-assistant-app.streamlit.app)
