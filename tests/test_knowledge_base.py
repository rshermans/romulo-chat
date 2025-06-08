import os
import json
from romulo_rag.knowledge_base import KnowledgeBase


def test_add_and_search(tmp_path):
    kb_file = tmp_path / "kb.jsonl"
    kb = KnowledgeBase(str(kb_file))
    kb.add_document("gatos adoram brincar com novelos de lã")
    kb.add_document("cachorros gostam de passear pela manhã")

    results = kb.search("gatos", top_k=1)
    assert len(results) == 1
    assert "gatos" in results[0]
