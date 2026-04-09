"""Architect Task - Designs Lua script architecture for FiveM."""

from crewai import Task, Agent

from src.models.schemas import ScriptArchitecture


def create_architect_task(agent: Agent) -> Task:
    """Create the architecture design task.
    
    Args:
        agent: The agent to assign this task to
        
    Returns:
        Task: Configured architecture task with structured output
    """
    return Task(
        description="""
        Based on the feature design, create a detailed technical architecture for the FiveM script.
        
        You must define:
        
        1. Resource name (lowercase, use hyphens, e.g., my-shop-script)
        
        2. For client.lua:
           - All client-side functions with clear purposes
           - Client events (RegisterNetEvent, AddEventHandler)
           - NUI callbacks if needed
           - Draw functions, threads, and loops
        
        3. For server.lua:
           - All server-side functions
           - Server events
           - Database queries (if applicable)
           - Security checks and validations
        
        4. For config.lua:
           - All configurable options
           - Default values
           - Locations, prices, items, etc.
        
        5. Shared variables and constants
        
        6. External dependencies (oxmysql, ox_lib, etc.)
        
        Follow FiveM best practices:
        - Use local functions when possible
        - Minimize global variables
        - Use proper event naming
        - Consider security implications
        """,
        expected_output=(
            "A complete script architecture detailing all files, functions, "
            "events, configuration options, and dependencies."
        ),
        agent=agent,
        output_pydantic=ScriptArchitecture,
    )
