"""Generate Code Task - Generates production-ready FiveM Lua code."""

from crewai import Task, Agent

from src.models.schemas import GeneratedCode


def create_generate_code_task(agent: Agent) -> Task:
    """Create the code generation task.
    
    Args:
        agent: The agent to assign this task to
        
    Returns:
        Task: Configured code generation task with structured output
    """
    return Task(
        description="""
        Based on the architecture design, generate complete, production-ready FiveM Lua code.
        
        Generate the following files:
        
        1. **client.lua**:
           - Framework initialization (CFX Default, ESX, or QBCore)
           - For CFX Default: use native FiveM functions only (no framework dependency)
           - All client-side functions
           - Event handlers with RegisterNetEvent and AddEventHandler
           - TriggerServerEvent calls
           - NUI handlers if needed
           - Threads and loops
           - Clean UI/UX interactions
        
        2. **server.lua**:
           - Framework initialization (or standalone for CFX Default)
           - For CFX Default: use native server functions, no framework required
           - All server-side functions
           - Event handlers
           - TriggerClientEvent calls
           - Database operations (using oxmysql patterns)
           - Security validations
           - Logging for admin actions
        
        3. **config.lua**:
           - Config = {} table
           - All configurable options with sensible defaults
           - Comments explaining each option
           - Locations as vector3/vector4
           - Prices, items, permissions, etc.
        
        4. **fxmanifest.lua**:
           - fx_version 'cerulean'
           - game 'gta5'
           - Proper file declarations
           - Dependencies
           - Metadata
        
        CODE REQUIREMENTS:
        - Use proper Lua syntax
        - Include error handling
        - Add brief comments for complex logic
        - Use local variables appropriately
        - Follow framework conventions exactly
        - NO placeholder code - everything must be complete
        - NO TODO comments
        - Code must work immediately when placed on a server
        """,
        expected_output=(
            "Complete, production-ready Lua code for all four files: "
            "client.lua, server.lua, config.lua, and fxmanifest.lua."
        ),
        agent=agent,
        output_pydantic=GeneratedCode,
    )
