from romulo_rag.markov_generator import build_chain, generate


def test_markov_generation_consistency():
    texts = ["ola mundo", "mundo azul"]
    chain = build_chain(texts, order=1)
    result = generate(chain, length=4)
    assert isinstance(result, str)
    assert len(result.split()) >= 1
