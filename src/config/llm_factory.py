"""LLM Factory - Creates LLM instances based on provider settings."""

from crewai import LLM

from src.config.settings import get_effective_settings


def create_llm() -> LLM:
    """Create LLM instance based on current provider settings.
    
    Returns:
        LLM: Configured LLM instance (Gemini or Ollama)
    """
    settings = get_effective_settings()
    provider = settings["llm_provider"]
    
    if provider == "ollama":
        return LLM(
            model=f"ollama/{settings['ollama_model_name']}",
            base_url=settings["ollama_base_url"],
        )
    else:
        return LLM(
            model=f"gemini/{settings['gemini_model_name']}",
            api_key=settings["google_api_key"],
        )


def get_current_provider_info() -> dict:
    """Get current provider information for display.
    
    Returns:
        dict: Provider info with name and model
    """
    settings = get_effective_settings()
    provider = settings["llm_provider"]
    
    if provider == "ollama":
        return {
            "provider": "ollama",
            "model": settings["ollama_model_name"],
            "base_url": settings["ollama_base_url"],
        }
    else:
        return {
            "provider": "gemini",
            "model": settings["gemini_model_name"],
            "api_key_set": bool(settings["google_api_key"]),
        }
