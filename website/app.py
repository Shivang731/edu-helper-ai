"""
Flask front-end for Edu Helper AI with Cursor-style UI/UX.
"""

import tempfile
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from werkzeug.utils import secure_filename

# Import your core and services modules
from core.fetcher import extract_text_from_pdf, extract_text_from_txt
from core.parser import StudyMaterialParser
from core.summarizer import generate_summary
from core.quizgen import generate_flashcards
from core.tts import text_to_speech
from services.embeddings import SemanticSearchService
from services.exporter import ExporterService

# Configuration
ALLOWED_EXTS = {"pdf", "txt"}
UPLOAD_DIR = Path(tempfile.gettempdir()) / "edu_helper_uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "change-me-in-production"


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not allowed_file(file.filename):
            flash("Please upload a PDF or TXT file.", "danger")
            return redirect(request.url)

        fname = secure_filename(file.filename)
        fpath = UPLOAD_DIR / fname
        file.save(fpath)

        # Extract text
        if fname.lower().endswith(".pdf"):
            raw = extract_text_from_pdf(open(fpath, "rb"))
        else:
            raw = extract_text_from_txt(open(fpath, "rb"))

        if raw.startswith("Error"):
            flash(raw, "danger")
            return redirect(request.url)

        # Clean & process
        parser = StudyMaterialParser()
        cleaned = parser.clean_extracted_text(raw)
        summary = generate_summary(cleaned)
        flashcards = generate_flashcards(cleaned, num_cards=10)

        # Semantic search
        search_engine = SemanticSearchService()
        search_engine.setup_index(cleaned)
        app.config["search_engine"] = search_engine

        # Store session data
        session["filename"] = fname
        session["summary"] = summary
        session["flashcards"] = flashcards
        return redirect(url_for("results"))

    return render_template("index.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    if "filename" not in session:
        return redirect(url_for("index"))

    query = None
    hits = None
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            engine = app.config.get("search_engine")
            hits = engine.search(query, top_k=5) if engine else []

    return render_template(
        "results.html",
        filename=session["filename"],
        summary=session["summary"],
        flashcards=session["flashcards"],
        query=query,
        hits=hits or []
    )


@app.route("/download/audio")
def download_audio():
    if "summary" not in session:
        return redirect(url_for("index"))
    mp3 = text_to_speech(session["summary"])
    if not mp3:
        flash("Audio generation failed.", "danger")
        return redirect(url_for("results"))
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(mp3)
    tmp.flush()
    return send_file(tmp.name, as_attachment=True, download_name="study_audio.mp3")


@app.route("/download/markdown")
def download_markdown():
    if "summary" not in session or "filename" not in session:
        return redirect(url_for("index"))
    exporter = ExporterService()
    md_path = exporter.export_summary_md(session["filename"], session["summary"])
    return send_file(md_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
