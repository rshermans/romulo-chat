from typing import List, Optional

from .knowledge_base import KnowledgeBase
from .markov_generator import build_chain, generate
from .config import AppConfig
from .llm_client import generate_with_llm


def generate_answer(
    query: str,
    kb: KnowledgeBase,
    *,
    config: Optional[AppConfig] = None,
    chain_order: int = 2,
    length: int = 50,
) -> str:
    """Retrieve documents related to query and generate a response."""

    docs: List[str] = kb.search(query, top_k=5)
    if not docs:
        return "Ainda nao tenho conhecimento sobre esse assunto."

    if config and config.data.get("provider", "markov") != "markov":
        provider = config.data.get("provider", "markov")
        key = config.get_api_key(provider) or ""
        context = "\n".join(docs)
        prompt = f"{context}\n\nUsuário: {query}\nAssistente:"
        return generate_with_llm(prompt, provider, key)

    chain = build_chain(docs, order=chain_order)
    response = generate(chain, length=length)
    return response
