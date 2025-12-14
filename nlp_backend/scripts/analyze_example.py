import json
import sys
from pathlib import Path
from nlp import analyze_document

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.analyze_example path/to/document.json")
        sys.exit(1)
    p = Path(sys.argv[1])
    if not p.exists():
        print("File not found:", p)
        sys.exit(2)
    doc = json.loads(p.read_text(encoding="utf-8"))

    # Use main API: analyze_document(title, body)
    title = doc.get("title", "") or ""
    body = doc.get("body", "") or ""
    tokens, entities = analyze_document(title, body)

    # attach results to doc and print
    doc["tokens"] = tokens
    doc["entities"] = {
        "PER": entities.get("PER", []),
        "ORG": entities.get("ORG", []),
        "LOC": entities.get("LOC", []),
        "DATE": entities.get("DATE", [])
    }

    print(json.dumps(doc, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()