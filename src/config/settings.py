"""Application settings using pydantic-settings."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM Provider
    llm_provider: Literal["gemini", "ollama"] = "gemini"

    # Google Gemini Configuration
    google_api_key: Optional[str] = None
    gemini_model_name: str = "gemini-1.5-pro"

    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model_name: str = "llama3"

    # Output Configuration
    output_dir: str = "output"


# Runtime settings file for web UI changes
RUNTIME_SETTINGS_FILE = Path("runtime_settings.json")


def load_runtime_settings() -> dict:
    """Load runtime settings from JSON file."""
    if RUNTIME_SETTINGS_FILE.exists():
        try:
            return json.loads(RUNTIME_SETTINGS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_runtime_settings(settings: dict) -> None:
    """Save runtime settings to JSON file."""
    RUNTIME_SETTINGS_FILE.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


def get_effective_settings() -> dict:
    """Get effective settings (env + runtime overrides)."""
    base = get_settings()
    runtime = load_runtime_settings()
    
    return {
        "llm_provider": runtime.get("llm_provider", base.llm_provider),
        "google_api_key": runtime.get("google_api_key", base.google_api_key),
        "gemini_model_name": runtime.get("gemini_model_name", base.gemini_model_name),
        "ollama_base_url": runtime.get("ollama_base_url", base.ollama_base_url),
        "ollama_model_name": runtime.get("ollama_model_name", base.ollama_model_name),
        "output_dir": base.output_dir,
    }
