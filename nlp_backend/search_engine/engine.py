import json
import math
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

class ParsedQuery:
    def __init__(self, query_text: str, tokens: List[str]):
        self.query_text = query_text
        self.tokens = tokens  # токени запиту

class SearchEngine:
    def __init__(self, db_filename: str = "data.json"):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.db_path = self.base_dir / db_filename

        print(f"🔍 SEARCH ENGINE: Використовую базу даних: {self.db_path}")

        # inverted index: token -> {doc_id: tf}
        self.index: Dict[str, Dict[str, int]] = defaultdict(dict)

        # documents storage
        self.documents: Dict[str, Dict[str, Any]] = {}

        self._load_db()

    # ===============================
    # Завантаження бази документів
    # ===============================
    def _load_db(self):
        if not self.db_path.exists():
            print(f"Файлу {self.db_path} не існує. Створюємо новий.")
            self._save_db()
            return

        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.documents.clear()
            self.index.clear()

            for doc in data:
                doc_id = doc.get("id")
                if not doc_id:
                    continue

                self.documents[doc_id] = doc

                # Токени тексту + заголовка
                tokens = []
                tokens.extend(doc.get("tokens", []))
                tokens.extend(doc.get("title_tokens", []))

                token_counts = Counter(tokens)
                for token, tf in token_counts.items():
                    self.index[token][doc_id] = tf

            print(f"✅ Завантажено {len(self.documents)} документів.")

        except Exception as e:
            print(f"❌ Помилка читання БД: {e}")

    # ===============================
    # Збереження БД
    # ===============================
    def _save_db(self):
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(list(self.documents.values()), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Помилка запису БД: {e}")

    # ===============================
    # Додавання документа
    # ===============================
    def add_document(self, doc: Dict[str, Any]):
        doc_id = doc["id"]
        self.documents[doc_id] = doc

        tokens = []
        tokens.extend(doc.get("tokens", []))
        tokens.extend(doc.get("title_tokens", []))

        token_counts = Counter(tokens)
        for token, tf in token_counts.items():
            self.index[token][doc_id] = tf

        self._save_db()

    # ===============================
    # Пошук з TF–IDF
    # ===============================
    def search(
        self,
        query: ParsedQuery,
        doc_type_filter: str = "all",
        entity_type_filter: str = "all",
    ) -> List[Dict[str, Any]]:

        if not query.tokens:
            return []

        scores: Dict[str, float] = defaultdict(float)
        N = len(self.documents)

        # ---------- TF–IDF ----------
        for token in query.tokens:
            if token not in self.index:
                continue

            df = len(self.index[token])
            idf = math.log((N + 1) / (df + 1)) + 1  # стабільний IDF

            for doc_id, tf in self.index[token].items():
                scores[doc_id] += tf * idf

        # ---------- Фільтрація + нормалізація ----------
        results = []

        for doc_id, score in scores.items():
            doc = self.documents.get(doc_id)
            if not doc:
                continue

            # фільтр типу документа
            if doc_type_filter != "all" and doc.get("doc_type") != doc_type_filter:
                continue

            # фільтр сутностей
            if entity_type_filter != "all":
                ents = doc.get("entities", {})
                if not ents.get(entity_type_filter):
                    continue

            # нормалізація за довжиною документа
            doc_len = len(doc.get("tokens", [])) + len(doc.get("title_tokens", []))
            norm_score = score / max(1, doc_len)

            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "snippet": doc.get("body", "")[:200] + "...",
                "score": round(norm_score, 4),
                "doc_type": doc.get("doc_type", "unknown"),
                "entities": doc.get("entities", {}),
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    # ===============================
    # Отримання документа
    # ===============================
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self.documents.get(doc_id)

engine = SearchEngine()