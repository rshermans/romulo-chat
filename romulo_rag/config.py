import json
from pathlib import Path
from typing import Dict, Optional


class AppConfig:
    """Manage provider configuration and API keys."""

    def __init__(self, path: str = "data/config.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data: Dict[str, object] = {"provider": "markov", "api_keys": {}}
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    self.data.update(json.load(f))
            except json.JSONDecodeError:
                pass

    def save(self) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f)

    def set_provider(self, provider: str) -> None:
        self.data["provider"] = provider
        self.save()

    def set_api_key(self, provider: str, key: str) -> None:
        self.data.setdefault("api_keys", {})[provider] = key
        self.save()

    def get_api_key(self, provider: str) -> Optional[str]:
        return self.data.get("api_keys", {}).get(provider)
