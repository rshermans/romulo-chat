from romulo_rag.config import AppConfig
from romulo_rag.knowledge_base import KnowledgeBase
from romulo_rag.rag import generate_answer


def test_config_save_and_load(tmp_path, monkeypatch):
    cfg_file = tmp_path / "config.json"
    cfg = AppConfig(str(cfg_file))
    cfg.set_provider("openai")
    cfg.set_api_key("openai", "TEST")

    loaded = AppConfig(str(cfg_file))
    assert loaded.data["provider"] == "openai"
    assert loaded.get_api_key("openai") == "TEST"

    kb_file = tmp_path / "kb.jsonl"
    kb = KnowledgeBase(str(kb_file))
    kb.add_document("ola mundo")

    def fake_llm(prompt, provider, api_key):
        return "LLM ok"

    monkeypatch.setattr("romulo_rag.rag.generate_with_llm", fake_llm)
    resp = generate_answer("ola", kb, config=loaded)
    assert resp == "LLM ok"
