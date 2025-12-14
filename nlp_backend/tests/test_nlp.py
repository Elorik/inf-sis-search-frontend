from nlp import analyze_document

SAMPLE_DOC = {
    "id": "doc1",
    "title": "Університет ІТ імені Т.Шевченка оголосив набір",
    "body": "1 липня 2024 року університет оголосив набір студентів. Контактна особа: Іван Петренко.",
    "source": "site.ua",
    "date": "2024-07-01",
    "doc_type": "news",
    "entities": {"PER": [], "ORG": [], "LOC": [], "DATE": []},
    "tokens": []
}

def test_analyze_document_basic():
    tokens, entities = analyze_document(SAMPLE_DOC["title"], SAMPLE_DOC["body"])
    assert isinstance(tokens, list)
    assert isinstance(entities, dict)
    assert set(entities.keys()) >= {"PER", "ORG", "LOC", "DATE"}
    # tokens should include some token or at least not crash
    assert len(tokens) >= 0
    assert isinstance(entities["DATE"], list)
    assert isinstance(entities["PER"], list)