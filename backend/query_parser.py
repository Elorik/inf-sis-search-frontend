import re
from typing import List
from models import ParsedQuery

def parse_query(raw: str) -> ParsedQuery:
    phrases = re.findall(r'"([^"]+)"', raw)
    cleaned = re.sub(r'"[^"]+"', "", raw)

    tokens = cleaned.split()
    must: List[str] = []
    should: List[str] = []
    must_not: List[str] = []

    current_op = "AND"  # за замовчуванням

    for token in tokens:
        up = token.upper()
        if up in {"AND", "OR", "NOT"}:
            current_op = up
            continue

        word = token
        if current_op == "NOT":
            must_not.append(word)
        elif current_op == "OR":
            should.append(word)
        else:
            must.append(word)

    return ParsedQuery(must=must, should=should, must_not=must_not, phrases=phrases)
