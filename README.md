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

## Supported Language Codes

The UI currently exposes a high-demand subset of NLLB codes. You can add more inside `SUPPORTED_LANGS` in `app/main.py`.

## Notes for Production

- Run behind a reverse proxy (Nginx/Caddy).
- Add Redis/S3 storage for translated file persistence.
- Add authentication and file-size guards.
- Preload translation model at startup for lower first-request latency.
- Add worker queue for large documents.
