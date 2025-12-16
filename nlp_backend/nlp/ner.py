import re
from typing import Dict, List

try:
    import spacy
    _HAS_SPACY = True
except Exception:
    _HAS_SPACY = False

# DATE regex: базова підтримка різних форматів
DATE_PATTERNS = [
    r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b",
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}\s+(?:січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)\s+\d{4}\b",
    r"\b\d{1,2}\s+(?:січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)\b",
]
DATE_RE = re.compile("|".join(DATE_PATTERNS), flags=re.IGNORECASE | re.UNICODE)

# Heuristic capitalized phrase matcher for PER/ORG/LOC
CAP_SEQ = re.compile(r"(?:\b[А-ЯІЇЄ][а-яіїє’'\-]+(?:\s+[А-ЯІЇЄ][а-яіїє’'\-]+){0,3})")

def _empty_entities_dict() -> Dict[str, List[str]]:
    return {"PER": [], "ORG": [], "LOC": [], "DATE": []}

class NER:
    def __init__(self, lang: str = "uk"):
        self.lang = lang
        self.nlp = None
        if _HAS_SPACY:
            try:
                if lang.startswith("uk"):
                    try:
                        self.nlp = spacy.load("uk_core_news_sm")
                    except Exception:
                        try:
                            self.nlp = spacy.load("xx_ent_wiki_sm")
                        except Exception:
                            self.nlp = None
                else:
                    self.nlp = spacy.load("en_core_web_sm")
            except Exception:
                self.nlp = None

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        ents = _empty_entities_dict()
        if not text or not text.strip():
            return ents

        # Dates by regex
        for m in DATE_RE.finditer(text):
            val = m.group(0).strip()
            if val not in ents["DATE"]:
                ents["DATE"].append(val)

        # If we have spaCy NER, use it and map labels
        if self.nlp:
            try:
                doc = self.nlp(text)
                for e in doc.ents:
                    label = e.label_.upper()
                    sval = e.text.strip()
                    if label in {"PERSON", "PER", "PERSONS"}:
                        if sval not in ents["PER"]:
                            ents["PER"].append(sval)
                    elif label in {"ORG", "ORGANIZATION", "COMPANY"}:
                        if sval not in ents["ORG"]:
                            ents["ORG"].append(sval)
                    elif label in {"GPE", "LOC", "LOCATION", "CITY", "COUNTRY"}:
                        if sval not in ents["LOC"]:
                            ents["LOC"].append(sval)
                    elif label in {"DATE", "TIME"}:
                        if sval not in ents["DATE"]:
                            ents["DATE"].append(sval)
            except Exception:
                # if spaCy fails for some reason, continue with heuristics
                pass

            return ents

        # Fallback heuristic: capitalized sequences (good for Ukrainian texts)
        for m in CAP_SEQ.finditer(text):
            tok = m.group(0).strip()
            lower = tok.lower()
            # Naive rules: org words -> ORG
            if any(x in lower for x in ["університет", "інститут", "компан", "завод", "фірм", "холдинг", "банк", "телеком"]):
                if tok not in ents["ORG"]:
                    ents["ORG"].append(tok)
            elif len(tok.split()) >= 2:
                if tok not in ents["PER"]:
                    ents["PER"].append(tok)
            else:
                if tok not in ents["LOC"]:
                    ents["LOC"].append(tok)

        return ents

_default_ner = NER(lang="uk")

def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Public function for extracting entities.
    Returns dict with exact keys: PER, ORG, LOC, DATE.
    """
    return _default_ner.extract_entities(text)