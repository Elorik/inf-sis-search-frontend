from typing import Literal
DocType = Literal["news", "opinion", "scientific"]

def classify_document(text: str) -> DocType:
    t = text.lower()
    if any(w in t for w in ["дослідження", "метод", "експеримент", "аналіз"]):
        return "scientific"
    if any(w in t for w in ["думка", "автор вважає", "на мою думку", "колонка"]):
        return "opinion"
    return "news"
