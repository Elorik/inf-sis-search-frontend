import math
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional


# Це структура, яку ми очікуємо від Поліводи (згідно з вимогами)
class ParsedQuery:
    def __init__(self, query_text: str, tokens: List[str]):
        self.query_text = query_text
        self.tokens = tokens  # Токенізований запит


class SearchEngine:
    def __init__(self):
        # Inverted Index: token -> {doc_id: term_frequency}
        self.index: Dict[str, Dict[str, int]] = defaultdict(dict)
        # Зберігаємо метадані документів для швидкого доступу при фільтрації та віддачі результату
        # id -> full_doc
        self.documents: Dict[str, Dict[str, Any]] = {}

    def add_document(self, doc: Dict[str, Any]):
        """
        Індексує документ.
        Очікує документ з полями: id, tokens, doc_type, entities, title, body...
        """
        doc_id = doc['id']
        self.documents[doc_id] = doc

        # Рахуємо частоту токенів у документі для ранжування
        token_counts = Counter(doc['tokens'])

        for token, count in token_counts.items():
            self.index[token][doc_id] = count

    def search(self,
               query: ParsedQuery,
               doc_type_filter: str = 'all',
               entity_type_filter: str = 'all') -> List[Dict[str, Any]]:
        """
        Основна логіка пошуку.
        1. Знаходить документи, що містять токени запиту.
        2. Фільтрує результати.
        3. Ранжує (сортує) за релевантністю (score).
        """
        if not query.tokens:
            return []

        # 1. Збір кандидатів (документи, які мають хоча б один токен)
        # score = сума входжень токенів (простий TF)
        scores: Dict[str, int] = defaultdict(int)

        for token in query.tokens:
            if token in self.index:
                for doc_id, tf in self.index[token].items():
                    scores[doc_id] += tf

        results = []

        # 2. Фільтрація та формування відповіді
        for doc_id, score in scores.items():
            doc = self.documents.get(doc_id)
            if not doc:
                continue

            # Фільтр по типу документа
            if doc_type_filter != 'all' and doc.get('doc_type') != doc_type_filter:
                continue

            # Фільтр по наявності сутностей певного типу
            # Якщо користувач шукає 'PER', то у документі має бути хоча б одна PER
            if entity_type_filter != 'all':
                ents = doc.get('entities', {})
                # Перевіряємо, чи є список сутностей для цього ключа і чи він не пустий
                if not ents.get(entity_type_filter):
                    continue

            # Додаємо в результат (формат згідно вимог 2.2)
            results.append({
                "id": doc['id'],
                "title": doc['title'],
                # Snippet поки заглушка, бо його генерує Полівода,
                # але тут ми просто повертаємо об'єкт.
                # У реальній інтеграції ми викличемо генератор сніпетів тут або на рівні API.
                "snippet": "",
                "score": score,
                "doc_type": doc.get('doc_type', 'unknown'),
                "entities": doc.get('entities', {})
            })

        # 3. Ранжування (від найбільшого score до найменшого)
        results.sort(key=lambda x: x['score'], reverse=True)

        return results

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self.documents.get(doc_id)


# Створюємо глобальний екземпляр двигуна
engine = SearchEngine()