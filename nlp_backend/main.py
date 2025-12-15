from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

# Імпортуємо наш двигун
from search_engine.engine import engine, ParsedQuery


# --- MOCK ЗАЛЕЖНОСТЕЙ ВІД ПОЛІВОДИ ---
# Оскільки Поліводи ще немає, ми емулюємо його функції тут.
# Коли Полівода дасть код, ми замінимо ці функції на імпорти.

def mock_parse_query(query: str) -> ParsedQuery:
    """
    Тимчасова функція. В реальності це буде:
    from polivoda_module import parse_query
    """
    # Простий спліт для тесту, поки немає NLP/Поліводи
    tokens = query.lower().split()
    return ParsedQuery(query_text=query, tokens=tokens)


def mock_generate_snippet(doc_body: str, query_tokens: List[str]) -> str:
    """
    Тимчасова функція. В реальності це буде:
    from polivoda_module import generate_snippet
    """
    return doc_body[:100] + "..."


# --- КІНЕЦЬ MOCK ---

app = FastAPI(title="Search Engine API")


# Моделі відповіді (Contract 2.2)
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


# Ендпоінт пошуку
@app.get("/search", response_model=List[SearchResult])
def search_documents(
        q: str = Query(..., min_length=1),
        doc_type: str = Query("all", enum=["all", "news", "opinion", "scientific"]),
        entity_type: str = Query("all", enum=["all", "PER", "ORG", "LOC", "DATE"])
):
    # 1. Парсинг запиту (через модуль Поліводи)
    parsed_query = mock_parse_query(q)

    # 2. Виконання пошуку (Литвинюк)
    raw_results = engine.search(parsed_query, doc_type, entity_type)

    # 3. Дозбагачення сніпетами (через модуль Поліводи)
    final_results = []
    for res in raw_results:
        # Дістаємо повне тіло документа з engine для генерації сніпета
        full_doc = engine.get_document(res['id'])
        if full_doc:
            # Викликаємо генератор сніпетів
            res['snippet'] = mock_generate_snippet(full_doc['body'], parsed_query.tokens)
        final_results.append(res)

    return final_results


# Ендпоінт для адмінки (додавання документів) - для тестування
# В реальності це викликатиме Полівода, але нам треба як закинути дані в engine.
class DocumentInput(BaseModel):
    id: str
    title: str
    body: str
    source: str
    date: str
    doc_type: str
    entities: EntityDict
    tokens: List[str]


@app.post("/admin/documents")
def add_document(doc: DocumentInput):
    # Конвертуємо Pydantic модель у dict
    doc_dict = doc.dict()
    # Додаємо в індекс
    engine.add_document(doc_dict)
    return {"status": "indexed", "id": doc.id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)