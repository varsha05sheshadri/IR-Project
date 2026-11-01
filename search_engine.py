import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LegalSearchEngine:
    """Ranks legal sections by TF-IDF cosine similarity."""
    def __init__(self, documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(
            lowercase=True, stop_words="english", ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.document_texts = [
            f'{d["act"]} {d["section"]} {d["title"]} {d["category"]} {d["text"]}'
            for d in documents
        ]
        self.matrix = self.vectorizer.fit_transform(self.document_texts)

    def search(self, query, category="All", limit=20):
        query = query.strip()
        if not query:
            return []
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).flatten()
        results = []
        for doc, score in zip(self.documents, scores):
            if category != "All" and doc["category"] != category:
                continue
            if score > 0:
                result = dict(doc)
                result["score"] = float(score)
                result["score_percent"] = round(float(score) * 100)
                result["snippet"] = self._snippet(doc["text"], query)
                results.append(result)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
@staticmethod
def _snippet(text, query, width=190):
    words = [w for w in re.findall(r"\w+", query.lower()) if len(w) > 2]
    lower = text.lower()

    positions = [lower.find(w) for w in words if lower.find(w) >= 0]

    if not positions:
        return text[:width] + ("…" if len(text) > width else "")

    start = max(0, min(positions) - 65)
    end = min(len(text), start + width)

    return ("…" if start else "") + text[start:end] + ("…" if end < len(text) else "")
