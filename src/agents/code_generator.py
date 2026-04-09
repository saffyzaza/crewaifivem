"""Code Generator Agent - Generates production-ready FiveM Lua code."""

from crewai import Agent

from src.config.llm_factory import create_llm


def create_code_generator_agent() -> Agent:
    """Create the Code Generator agent.
    
    This agent generates production-ready Lua code:
    - client.lua with client-side logic
    - server.lua with server-side logic
    - config.lua with configuration options
    - fxmanifest.lua with resource manifest
    
    Returns:
        Agent: Configured Code Generator agent
    """
    return Agent(
        role="FiveM Lua Code Generator",
        goal=(
            "Generate production-ready, clean, and well-documented FiveM Lua "
            "code based on the designed architecture. Ensure all code follows "
            "FiveM conventions and is immediately usable on a server."
        ),
        backstory=(
            "You are an expert FiveM Lua developer who writes clean, efficient, "
            "and production-ready code. You master vanilla CFX/FiveM native "
            "functions and also have extensive experience with ESX and QBCore "
            "frameworks. You prefer using native FiveM functions for standalone "
            "scripts. Your code is always well-structured, properly commented, "
            "and follows the DRY principle. You never leave TODO comments or "
            "placeholder code - everything you generate is complete and functional."
        ),
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
    )
