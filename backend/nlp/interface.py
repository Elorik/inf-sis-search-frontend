from typing import Dict, Any, Tuple, List
from .preprocessing import preprocess_text
from .ner import extract_entities

def analyze_document(title: str, body: str) -> Tuple[List[str], Dict[str, list]]:
    text = ((title or "") + " " + (body or "")).strip()
    tokens = preprocess_text(text)
    entities = extract_entities(text)

    return tokens, {
        "PER": entities.get("PER", []),
        "ORG": entities.get("ORG", []),
        "LOC": entities.get("LOC", []),
        "DATE": entities.get("DATE", []),
    }

def analyze_document_from_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    title = doc.get("title", "") or ""
    body = doc.get("body", "") or ""
    tokens, entities = analyze_document(title, body)

    out = dict(doc)
    out["tokens"] = tokens
    out["entities"] = {
        "PER": entities.get("PER", []),
        "ORG": entities.get("ORG", []),
        "LOC": entities.get("LOC", []),
        "DATE": entities.get("DATE", []),
    }
    return out
