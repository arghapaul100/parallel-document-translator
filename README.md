# Parallel Document Translator

Production-ready starter for a **free side-by-side DOCX translator** that keeps the document structure (paragraphs, tables, headers, and footers) while translating content from one language to another.

## Features

- Side-by-side preview of source and translated text.
- DOCX ingestion and DOCX export.
- Structure-preserving translation workflow (paragraph and table structure retained).
- FastAPI backend with Jinja frontend.
- Offline-capable open model approach via Hugging Face NLLB-200.

## Tech Stack

- FastAPI + Uvicorn
- python-docx for Word document parsing/rebuilding
- Transformers (NLLB-200 distilled 600M) for free multilingual translation

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000`.

## Windows Setup (if `venv` fails with `No module named 'encodings'`)

If you see an error like:

```text
Could not find platform independent libraries <prefix>
Fatal Python error: Failed to import encodings module
ModuleNotFoundError: No module named 'encodings'
```

this usually means your Python installation is broken or environment variables are pointing to the wrong Python home.

### 1) Verify Python installation path

In **Command Prompt**:

```bat
where python
python -c "import sys; print(sys.executable); print(sys.prefix)"
```

If this points to an unexpected/old install, uninstall it and reinstall Python from python.org.

### 2) Reinstall Python correctly

- Download a fresh installer from: https://www.python.org/downloads/windows/
- During install, check **Add Python to PATH**.
- Choose **Customize installation** and ensure standard library is included.
- Prefer installing for your user (or all users, but keep one clean install).

### 3) Clean conflicting environment variables

Remove `PYTHONHOME` and `PYTHONPATH` if they are set to stale paths:

```bat
set PYTHONHOME=
set PYTHONPATH=
```

Then open a **new terminal** and run:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4) If still broken, use the Python Launcher explicitly

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Supported Language Codes

The UI currently exposes a high-demand subset of NLLB codes. You can add more inside `SUPPORTED_LANGS` in `app/main.py`.

## Notes for Production

- Run behind a reverse proxy (Nginx/Caddy).
- Add Redis/S3 storage for translated file persistence.
- Add authentication and file-size guards.
- Preload translation model at startup for lower first-request latency.
- Add worker queue for large documents.
