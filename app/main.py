from __future__ import annotations

from io import BytesIO
from uuid import uuid4

from docx import Document
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.services.document import collect_document_paragraphs, translate_document
from app.services.translator import TranslationEngine

app = FastAPI(title="Parallel Document Translator", version="1.0.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
translator = TranslationEngine()
download_store: dict[str, dict[str, bytes | str]] = {}

SUPPORTED_LANGS = {
    "eng_Latn": "English",
    "fra_Latn": "French",
    "spa_Latn": "Spanish",
    "deu_Latn": "German",
    "hin_Deva": "Hindi",
    "zho_Hans": "Chinese (Simplified)",
    "arb_Arab": "Arabic",
    "rus_Cyrl": "Russian",
    "jpn_Jpan": "Japanese",
    "por_Latn": "Portuguese",
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {"results": [], "download_token": None, "languages": SUPPORTED_LANGS},
    )


@app.post("/translate", response_class=HTMLResponse)
async def translate(
    request: Request,
    file: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...),
) -> HTMLResponse:
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported.")

    file_bytes = await file.read()
    document = Document(BytesIO(file_bytes))
    refs = collect_document_paragraphs(document)
    if not refs:
        raise HTTPException(status_code=400, detail="No translatable text found in this document.")

    translated_texts = translator.translate_texts(
        [ref.source_text for ref in refs],
        source_lang=source_lang,
        target_lang=target_lang,
    )

    translated_doc = translate_document(file_bytes, translated_texts)
    token = str(uuid4())
    download_store[token] = {
        "data": translated_doc,
        "filename": f"translated_{file.filename}",
    }

    results = [
        {"source": ref.source_text, "translated": translated}
        for ref, translated in zip(refs, translated_texts, strict=True)
    ]

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "results": results,
            "download_token": token,
            "languages": SUPPORTED_LANGS,
        },
    )


@app.get("/download/{token}")
async def download(token: str):
    payload = download_store.get(token)
    if not payload:
        raise HTTPException(status_code=404, detail="Translated file expired or missing.")

    return StreamingResponse(
        BytesIO(payload["data"]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={payload['filename']}"},
    )
