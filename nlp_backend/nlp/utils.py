from typing import Dict, Any

def validate_document_structure(doc: Dict[str, Any]) -> bool:
    """
    Checks that the document roughly follows required schema.
    """
    required = {"id", "title", "body", "source", "date", "doc_type", "entities", "tokens"}
    return required.issubset(set(doc.keys()))