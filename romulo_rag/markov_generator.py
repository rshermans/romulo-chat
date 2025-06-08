import random
from collections import defaultdict
from typing import List, Tuple, Dict


def build_chain(texts: List[str], order: int = 2) -> Dict[Tuple[str, ...], List[str]]:
    chain: Dict[Tuple[str, ...], List[str]] = defaultdict(list)
    for text in texts:
        words = text.split()
        if len(words) < order + 1:
            continue
        for i in range(len(words) - order):
            key = tuple(words[i : i + order])
            chain[key].append(words[i + order])
    return chain


def generate(chain: Dict[Tuple[str, ...], List[str]], length: int = 50) -> str:
    if not chain:
        return ""
    start = random.choice(list(chain.keys()))
    words = list(start)
    for _ in range(length - len(start)):
        key = tuple(words[-len(start) :])
        next_words = chain.get(key)
        if not next_words:
            break
        words.append(random.choice(next_words))
    return " ".join(words)
