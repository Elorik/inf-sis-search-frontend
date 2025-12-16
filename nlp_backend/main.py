from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel
import re
from nlp.interface import analyze_document
from search_engine.engine import engine, ParsedQuery
from fastapi.middleware.cors import CORSMiddleware


def classify_document(text: str) -> str:
    """
    Автоматична класифікація документа:
    news / publicistic / scientific
    """
    t = text.lower()

    if any(w in t for w in ["дослідження", "метод", "експеримент", "висновки", "результати"]):
        return "scientific"
    if any(w in t for w in ["сьогодні", "повідомляє", "заявив", "новини", "пресслужба"]):
        return "news"
    return "publicistic"


def parse_query(raw_query: str) -> ParsedQuery:
    """
    Парсер пошукового запиту.
    Підтримує:
    - AND, OR, NOT
    - фрази в лапках
    """
    raw_query = raw_query.strip()
    phrases = re.findall(r'"([^"]+)"', raw_query)
    rest = re.sub(r'"[^"]+"', "", raw_query)
    tokens = []
    for part in rest.split():
        up = part.upper()
        if up not in {"AND", "OR", "NOT"}:
            tokens.append(part.lower())
    tokens.extend([p.lower() for p in phrases])
    return ParsedQuery(query_text=raw_query, tokens=tokens)

def generate_snippet(text: str, query_tokens: List[str], max_len: int = 160) -> str:

    if not text:
        return ""

    lower = text.lower()
    for token in query_tokens:
        pos = lower.find(token.lower())
        if pos != -1:
            start = max(0, pos - 50)
            end = min(len(text), pos + max_len)
            return "..." + text[start:end].replace("\n", " ") + "..."
    return text[:max_len].replace("\n", " ") + "..."

app = FastAPI(title="Search Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EntityDict(BaseModel):
    PER: List[str] = []
    ORG: List[str] = []
    LOC: List[str] = []
    DATE: List[str] = []

class SearchResult(BaseModel):
    id: str
    title: str
    snippet: str
    score: float
    doc_type: str
    entities: EntityDict

class DocumentInput(BaseModel):
    id: str
    title: str
    body: str
    source: str
    date: str


@app.get("/search", response_model=List[SearchResult])
def search_documents(
    q: str = Query(..., min_length=1),
    doc_type: str = Query("all", enum=["all", "news", "publicistic", "scientific"]),
    entity_type: str = Query("all", enum=["all", "PER", "ORG", "LOC", "DATE"])
):


    parsed_query = parse_query(q)
    raw_results = engine.search(parsed_query, doc_type, entity_type)

    final_results = []
    for res in raw_results:
        full_doc = engine.get_document(res["id"])
        if full_doc:
            res["snippet"] = generate_snippet(full_doc.get("body", ""), parsed_query.tokens)
        final_results.append(res)
    return final_results


@app.post("/admin/documents")
def add_document(doc: DocumentInput):
    # Аналіз та збереження
    tokens, entities = analyze_document(doc.title, doc.body)
    doc_type = classify_document(doc.title + " " + doc.body)

    doc_dict = {
        "id": doc.id,
        "title": doc.title,
        "body": doc.body,
        "source": doc.source,
        "date": doc.date,
        "doc_type": doc_type,
        "tokens": tokens,
        "entities": entities
    }

    engine.add_document(doc_dict)

    return {
        "status": "indexed",
        "id": doc.id,
        "file_saved_to": str(engine.db_path)
    }


@app.get("/admin/db-dump")
def get_database_dump():
    return {
        "status": "ok",
        "db_path": str(engine.db_path),
        "documents_count": len(engine.documents),
        "documents": engine.documents
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)