import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional


class ParsedQuery:
    def __init__(self, query_text: str, tokens: List[str]):
        self.query_text = query_text
        self.tokens = tokens  # Токенізований запит


class SearchEngine:
    def __init__(self, db_filename: str = "data.json"):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.db_path = self.base_dir / db_filename

        print(f"🔍 SEARCH ENGINE: Використовую базу даних: {self.db_path}")

        self.index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.documents: Dict[str, Dict[str, Any]] = {}
        self._load_db()

    def _load_db(self):
        if not self.db_path.exists():
            print(f"Файлу {self.db_path} не існує. Створюємо новий пустий файл.")
            self._save_db()
            return

        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.documents = {}
            self.index = defaultdict(dict)

            for doc in data:
                doc_id = doc.get('id')
                if not doc_id: continue

                self.documents[doc_id] = doc
                token_counts = Counter(doc.get('tokens', []))
                for token, count in token_counts.items():
                    self.index[token][doc_id] = count

            print(f"Успішно завантажено {len(self.documents)} документів.")

        except Exception as e:
            print(f"Помилка читання БД: {e}")

    def _save_db(self):
        try:
            docs_list = list(self.documents.values())
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(docs_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Помилка запису в БД: {e}")

    def add_document(self, doc: Dict[str, Any]):
        doc_id = doc['id']
        self.documents[doc_id] = doc

        token_counts = Counter(doc['tokens'])
        for token, count in token_counts.items():
            self.index[token][doc_id] = count

        self._save_db()

    def search(self, query: ParsedQuery, doc_type_filter: str = 'all', entity_type_filter: str = 'all') -> List[
        Dict[str, Any]]:
        if not query.tokens:
            return []

        scores: Dict[str, int] = defaultdict(int)

        for token in query.tokens:
            if token in self.index:
                for doc_id, tf in self.index[token].items():
                    scores[doc_id] += tf

        results = []
        for doc_id, score in scores.items():
            doc = self.documents.get(doc_id)
            if not doc:
                continue

            if doc_type_filter != 'all' and doc.get('doc_type') != doc_type_filter:
                continue

            if entity_type_filter != 'all':
                ents = doc.get('entities', {})
                if not ents.get(entity_type_filter):
                    continue

            results.append({
                "id": doc['id'],
                "title": doc['title'],
                "snippet": "",
                "score": score,
                "doc_type": doc.get('doc_type', 'unknown'),
                "entities": doc.get('entities', {})
            })

        results.sort(key=lambda x: x['score'], reverse=True)

        return results

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self.documents.get(doc_id)


engine = SearchEngine()