"""Analyze Task - Analyzes user requirements for FiveM scripts."""

from crewai import Task, Agent

from src.models.schemas import RequirementAnalysis


def create_analyze_task(agent: Agent, user_requirement: str) -> Task:
    """Create the requirement analysis task.
    
    Args:
        agent: The agent to assign this task to
        user_requirement: Raw user requirement string
        
    Returns:
        Task: Configured analysis task with structured output
    """
    return Task(
        description=f"""
        Analyze the following FiveM script requirement and extract key information:
        
        USER REQUIREMENT:
        {user_requirement}
        
        You must:
        1. Identify the script name and type (job, shop, system, vehicle, housing, etc.)
        2. Determine the target framework based on context clues
           - If user mentions ESX-specific terms (es_extended, xPlayer), choose ESX
           - If user mentions QBCore-specific terms (QBCore, PlayerData), choose QBCore
           - If unclear or user wants standalone, default to CFX_DEFAULT (vanilla FiveM)
        3. List all core features mentioned or implied
        4. Assess target audience (beginner servers, advanced RP, etc.)
        5. Evaluate complexity level (simple, medium, complex)
        
        Be thorough but concise. Focus on extractable, actionable information.
        """,
        expected_output=(
            "A structured analysis containing script name, type, framework choice, "
            "core features list, target audience, and complexity assessment."
        ),
        agent=agent,
        output_pydantic=RequirementAnalysis,
    )
