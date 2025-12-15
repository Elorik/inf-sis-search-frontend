from typing import List

def generate_snippet(body: str, query_terms: List[str], max_len: int = 200) -> str:
    if not body:
        return ""

    lower_body = body.lower()
    positions = []

    for term in query_terms:
        pos = lower_body.find(term.lower())
        if pos != -1:
            positions.append(pos)

    start = 0
    if positions:
        center = min(positions)
        start = max(0, center - max_len // 2)

    snippet = body[start:start + max_len]
    if start > 0:
        snippet = "..." + snippet
    if start + max_len < len(body):
        snippet = snippet + "..."

    return snippet
