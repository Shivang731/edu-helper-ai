Here’s a **more human, inviting, and conversational version** of your README that still covers everything while making it easier to follow, especially for students or first-time users:

---

# 📚 Edu Helper

Welcome to your new AI-powered study buddy! This project helps you **turn textbooks, class notes, or articles** into bite-sized summaries, interactive flashcards, and even audio notes — perfect for learning on the go.

---

## ✨ What This Does

Think of it as a personal tutor that can:

* 📝 **Summarize PDFs & notes** using powerful AI
* 🃏 **Generate flashcards** from your material (fill-in-the-blank, Q\&A style)
* 🔊 **Turn summaries into audio** for hands-free review
* 🔍 **Answer questions** about your notes (semantic search!)
* 📤 **Export** your study materials in multiple formats
* 🎨 **Looks good while doing it** – modern, minimal UI with Cursor-like vibes

---

## 🧠 Who Is It For?

This is built for:

* Students (school/college)
* Competitive exam takers
* Self-learners
* Anyone who studies from PDFs or online notes

You don't need to be a coder to use it once it's running.

---

## 🏗️ How It’s Built (Project Structure)

```
edu-helper/
├── app/                 # Streamlit application entry point
│   └── main.py         # Main application file
├── core/               # Core processing logic
│   ├── fetcher.py      # PDF/TXT text extraction
│   ├── parser.py       # Text cleaning and preprocessing
│   ├── summarizer.py   # AI-powered summarization (BART)
│   ├── quizgen.py      # Flashcard and quiz generation
│   └── tts.py          # Text-to-speech conversion
├── services/           # External service integrations
│   ├── embeddings.py   # Semantic search (sentence-transformers + FAISS)
│   ├── storage.py      # SQLite database operations
│   └── exporter.py     # Export functionality
├── ui/                 # User interface components
│   ├── sidebar.py      # File upload and settings sidebar
│   ├── views.py        # Main content display components
│   └── controls.py     # Interactive controls and buttons
├── requirements.txt    # Python dependencies
└── README.md          # This file

```

---

## 🚀 How to Run This on Your Computer

### ✅ Step 1: Setup

Make sure you have:

* **Python 3.9+** (works best with 3.13.5)
* `pip` (comes with Python)

### 🔧 Step 2: Install It

```bash
# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install required packages
pip install -r requirements.txt
```

You can also install a spaCy model for better language processing:

```bash
python -m spacy download en_core_web_sm
```

---

### ▶️ Step 3: Run the App

```bash
streamlit run app/main.py
```

Then open your browser and go to: [http://localhost:8501](http://localhost:8501)

---

## 🧪 How to Use It (Once Running)

1. **Upload your PDF or TXT file**
2. Choose what you want:

   * 📝 Summary
   * 🃏 Flashcards
   * 🔊 Audio Notes
   * 🔍 Ask Questions
3. Export your content if needed (Markdown, Anki, etc.)
4. Study smarter. Repeat. 🧠

---

## 📌 Tips for Best Results

* Avoid scanned PDFs — use digital text-based files
* Shorter files = faster, smoother experience
* For long docs, use longer summary & more flashcards

---

## ❓ Common Issues & Fixes

| Problem                    | Fix                                        |
| -------------------------- | ------------------------------------------ |
| `ModuleNotFoundError`      | Run `pip install -r requirements.txt`      |
| "Model downloading…" stuck | Be patient – first run downloads AI models |
| PDF doesn’t work           | Try another file, avoid scanned PDFs       |
| Audio not working          | Check internet (Google TTS needs it)       |

---

## 🎨 UI Highlights

* Clean layout inspired by [Cursor](https://cursor.so/)
* Dark theme support
* Animated controls and transitions
* Sidebar-based workflow for simplicity

---

## 🧠 How It Works Behind the Scenes

* **Summarization**: Uses Hugging Face's BART model
* **Flashcards**: Generates cloze (fill-in-the-blank) and QA cards
* **Audio**: Powered by `gTTS` (Google Text-to-Speech)
* **Search**: Semantic search via FAISS + sentence-transformers
* **Storage**: SQLite keeps your sessions cached locally

---

## 🔒 Privacy Notes

* Everything runs locally — your files stay on your device
* No tracking, no cloud sync, no funny business

---

## 🤝 Want to Contribute?

Totally welcome! You can:

* Improve UI
* Add new features (e.g., more export options)
* Fix bugs or make it faster
* Share feedback

Just fork this repo, make changes, and open a PR.

---

## 📜 License & Use

This project is for **educational use**. Don’t upload copyrighted or sensitive content.

---

## 💬 Need Help?

* Check this README again
* Make sure your Python version is 3.9+
* Dependencies not working? Try deleting `venv` and reinstalling
* Still stuck? Open an issue or drop a message

---

> "Study smarter, not harder. Let AI do the boring bits."
> — Your future self 😄

---


