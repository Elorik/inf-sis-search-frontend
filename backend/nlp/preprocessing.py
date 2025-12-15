import re
from typing import List

try:
    import spacy
    _HAS_SPACY = True
except Exception:
    _HAS_SPACY = False

DEFAULT_STOPWORDS_UK = {
    "і", "в", "на", "з", "до", "та", "що", "не", "я", "у", "за",
    "це", "цею", "цей", "він", "вона", "вони", "ми", "ви", "їх", "її", "року", "років"
}

RE_WORD = re.compile(r"[А-Яа-яЁёA-Za-z0-9\-']+", flags=re.UNICODE)

class Preprocessor:
    def __init__(self, lang: str = "uk"):
        self.lang = lang
        self.stopwords = DEFAULT_STOPWORDS_UK if lang.startswith("uk") else set()
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
                            self.nlp = spacy.blank("uk")
                else:
                    self.nlp = spacy.load("en_core_web_sm")
            except Exception:
                self.nlp = None

    def preprocess_text(self, text: str) -> List[str]:
        if not text:
            return []
        words = RE_WORD.findall(text.replace("\n", " ").replace("\r", " ").strip())

        if self.nlp:
            try:
                doc = self.nlp(" ".join(words))
                out: List[str] = []
                for tok in doc:
                    lemma = (getattr(tok, "lemma_", None) or tok.text).lower().strip()
                    if not lemma or lemma in self.stopwords:
                        continue
                    out.append(lemma)
                return out
            except Exception:
                pass

        out: List[str] = []
        for w in words:
            lw = w.lower()
            if lw in self.stopwords:
                continue
            out.append(lw)
        return out

_default_prep = Preprocessor(lang="uk")

def preprocess_text(text: str) -> List[str]:
    return _default_prep.preprocess_text(text)
