from typing import Dict, Any, Tuple, List
from .preprocessing import preprocess_text
from .ner import extract_entities

REQUIRED_FIELDS = {"id", "title", "body", "source", "date", "doc_type", "entities", "tokens"}

def analyze_document(title: str, body: str) -> Tuple[List[str], Dict[str, list]]:
    """
    Основний інтерфейс (відповідно до вимог):
      - Приймає title та body (рядки)
      - Повертає (tokens, entities)
        tokens: List[str]
        entities: {"PER":[], "ORG":[], "LOC":[], "DATE": []}
    Це функція, яку викликає Полівода при додаванні документа.
    """
    text_for_tokens = ""
    if title:
        text_for_tokens += title + " "
    if body:
        text_for_tokens += body

    tokens = preprocess_text(text_for_tokens)
    entities = extract_entities(text_for_tokens)

    # Ensure consistent keys/values
    entities_out = {
        "PER": entities.get("PER", []),
        "ORG": entities.get("ORG", []),
        "LOC": entities.get("LOC", []),
        "DATE": entities.get("DATE", [])
    }

    return tokens, entities_out

# Compatibility helper: accept whole doc dict and return updated doc (useful for scripts/tests)
def analyze_document_from_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Backwards-compatible helper: приймає повний документ (dict),
    застосовує analyze_document(title, body) та повертає новий dict з заповненими
    полями 'tokens' та 'entities' (не змінює інші назви полів).
    """
    if not isinstance(doc, dict):
        raise ValueError("Document must be a dict.")
    title = doc.get("title", "") or ""
    body = doc.get("body", "") or ""

    tokens, entities = analyze_document(title, body)

    out = dict(doc)  # shallow copy
    out["tokens"] = tokens
    out["entities"] = {
        "PER": entities.get("PER", []),
        "ORG": entities.get("ORG", []),
        "LOC": entities.get("LOC", []),
        "DATE": entities.get("DATE", [])
    }
    return out