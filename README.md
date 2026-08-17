# 📚 Smart Study Assistant

A simple AI-powered study tool built with **Streamlit** and the **Gemini API**.

Paste in your notes, an article, or any text, and:
- **Summarize** it into key bullet points
- **Generate a quiz** to test your understanding
- **Ask follow-up questions** about the material in a chat interface

Built as part of a mini project exploring AI tools for coding, research, and productivity.

## Features

- 📝 One-click summarization of long notes/articles
- ❓ Auto-generated quiz questions with an answer key
- 💬 Chat-based Q&A grounded in your pasted text
- 🔑 Bring your own free Gemini API key — no server-side key storage

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Gemini API](https://ai.google.dev/) (`google-genai` SDK) — text generation
- Python 3.9+

## Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd smart-study-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a free Gemini API key**
   Grab one from [Google AI Studio](https://aistudio.google.com/apikey).

4. **Set your API key** (either works)
   - Paste it directly into the app's sidebar when it's running, **or**
   - Copy `.env.example` to `.env` and add your key, then export it:
     ```bash
     export GEMINI_API_KEY="your_key_here"
     ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`.

## How It Works

The app uses Gemini's `interactions.create()` endpoint to send your pasted
text along with a task-specific prompt (summarize / quiz / answer question),
and displays the model's response directly in the Streamlit UI.

## Screenshot

_Add a screenshot or GIF of the app here once it's running._

## What I Learned

_A few sentences on what you learned about prompting, AI APIs, or building
with Streamlit — good material for your LinkedIn post!_

## License

MIT
