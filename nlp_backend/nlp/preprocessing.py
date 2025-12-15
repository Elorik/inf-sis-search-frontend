import re
from typing import List

# Try to import spaCy (preferred). If not installed, we'll use fallback.
try:
    import spacy
    _HAS_SPACY = True
except Exception:
    _HAS_SPACY = False

# Minimal stopwords for Ukrainian (extendable).
DEFAULT_STOPWORDS_UK = {
    "і", "в", "на", "з", "до", "та", "що", "не", "я", "у", "за",
    "це", "цею", "цей", "він", "вона", "вони", "ми", "ви", "їх", "її", "року", "років"
}

RE_WORD = re.compile(r"\w+", flags=re.UNICODE)

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
                            # blank pipeline for lemmatization when model not present
                            self.nlp = spacy.blank("uk")
                else:
                    self.nlp = spacy.load("en_core_web_sm")
            except Exception:
                self.nlp = None

    def preprocess_text(self, text: str) -> List[str]:
        """
        Return list of normalized tokens (lemmas if available), lowercase, without stopwords.
        """
        if not text:
            return []

        text = text.strip()
        text = text.replace("\n", " ").replace("\r", " ")
        words = RE_WORD.findall(text)

        if self.nlp:
            try:
                doc = self.nlp(" ".join(words))
                tokens = []
                for tok in doc:
                    # Prefer lemma when available
                    lemma = getattr(tok, "lemma_", None)
                    if lemma:
                        lemma = lemma.lower().strip()
                    else:
                        lemma = tok.text.lower().strip()

                    if not lemma:
                        continue
                    if lemma in self.stopwords:
                        continue
                    # keep numeric tokens as-is (they might be useful)
                    tokens.append(lemma)
                return tokens
            except Exception:
                # fallback to simple path if spacy fails
                pass

        # fallback: lowercase, remove stopwords, simple normalization
        tokens = []
        for w in words:
            lw = w.lower()
            if lw in self.stopwords:
                continue
            tokens.append(lw)
        return tokens

# Convenience function
_default_prep = Preprocessor(lang="uk")

def preprocess_text(text: str) -> List[str]:
    return _default_prep.preprocess_text(text)