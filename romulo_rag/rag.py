from typing import List

from .knowledge_base import KnowledgeBase
from .markov_generator import build_chain, generate


def generate_answer(query: str, kb: KnowledgeBase, *, chain_order: int = 2, length: int = 50) -> str:
    """Retrieve documents related to query and generate a response."""
    docs: List[str] = kb.search(query, top_k=5)
    if not docs:
        return "Ainda nao tenho conhecimento sobre esse assunto."
    chain = build_chain(docs, order=chain_order)
    response = generate(chain, length=length)
    return response
