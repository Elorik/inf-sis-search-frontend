import json
from pathlib import Path
import uuid

from nlp.interface import analyze_document
from classifier import classify_document

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "documents.json"


def _load_raw_documents() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_raw_documents(docs: list[dict]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)


def add_document(payload: dict) -> dict:
    docs = _load_raw_documents()

    title = payload.get("title", "")
    body = payload.get("body", "")

    tokens, entities = analyze_document(title, body)

    doc = {
        "id": str(uuid.uuid4()),
        "title": title,
        "body": body,
        "source": payload.get("source", ""),
        "date": payload.get("date", ""),
        "doc_type": classify_document(body),
        "tokens": tokens,
        "entities": entities,
    }

    docs.append(doc)
    _save_raw_documents(docs)
    return doc


def load_documents() -> list[dict]:
    return _load_raw_documents()
