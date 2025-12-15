from data_layer import load_documents
from snippet_generator import generate_snippet

def search_documents(
    query: str,
    doc_type: str = "all",
    entity_type: str = "all",
    entity_value: str = "",
):
    docs = load_documents()
    results = []

    q = query.lower().strip()

    for doc in docs:
        if q and q not in doc["title"].lower() and q not in doc["body"].lower():
            continue

        if doc_type != "all" and doc["doc_type"] != doc_type:
            continue

        snippet = generate_snippet(doc["body"], [q] if q else [])

        results.append({
            "id": doc["id"],
            "title": doc["title"],
            "snippet": snippet,
            "doc_type": doc["doc_type"],
            "entities": doc.get("entities", {}),
            "score": 1.0
        })

    return results
