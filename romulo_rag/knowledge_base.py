import json
from pathlib import Path
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KnowledgeBase:
    """Simple knowledge base backed by a JSONL file."""

    def __init__(self, path: str = "data/knowledge.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.documents: List[str] = []
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        self.documents.append(obj.get("text", ""))
                    except json.JSONDecodeError:
                        # ignore corrupted lines
                        continue

    def add_document(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        self.documents.append(text)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"text": text}) + "\n")

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if not self.documents:
            return []
        corpus = self.documents + [query]
        vectorizer = TfidfVectorizer().fit(corpus)
        vecs = vectorizer.transform(corpus)
        sims = cosine_similarity(vecs[-1], vecs[:-1]).flatten()
        ranked_indices = sims.argsort()[::-1][:top_k]
        return [self.documents[i] for i in ranked_indices]
