"""Lua Architect Agent - Designs script architecture for FiveM."""

from crewai import Agent

from src.config.llm_factory import create_llm


def create_lua_architect_agent() -> Agent:
    """Create the Lua Architect agent.
    
    This agent designs the technical architecture:
    - File structure planning
    - Function definitions
    - Event architecture
    - Framework integration patterns
    
    Returns:
        Agent: Configured Lua Architect agent
    """
    return Agent(
        role="FiveM Lua Architect",
        goal=(
            "Design clean, maintainable, and efficient Lua script architecture "
            "for FiveM resources. Create clear separation between client and "
            "server logic while ensuring proper event communication."
        ),
        backstory=(
            "You are a senior Lua architect specializing in FiveM development. "
            "You have contributed to major frameworks like ESX and QBCore. "
            "You understand the importance of clean code architecture, proper "
            "event handling, and efficient client-server communication. You "
            "always follow FiveM best practices and ensure scripts are optimized "
            "for production use."
        ),
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
    )
