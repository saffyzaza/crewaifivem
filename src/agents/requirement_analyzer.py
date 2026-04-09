"""Requirement Analyzer Agent - Analyzes user requirements for FiveM scripts."""

from crewai import Agent

from src.config.llm_factory import create_llm


def create_requirement_analyzer_agent() -> Agent:
    """Create the Requirement Analyzer agent.
    
    This agent analyzes user requirements and extracts:
    - Script type and purpose
    - Target framework (ESX/QBCore)
    - Core features needed
    - Complexity assessment
    
    Returns:
        Agent: Configured Requirement Analyzer agent
    """
    return Agent(
        role="FiveM Requirement Analyst",
        goal=(
            "Analyze user requirements for FiveM scripts and extract clear, "
            "actionable specifications including script type, framework choice, "
            "and core features needed."
        ),
        backstory=(
            "You are an expert FiveM developer with years of experience in "
            "vanilla CFX/FiveM scripting, ESX, and QBCore frameworks. You have "
            "deep understanding of FiveM server architecture and native functions. "
            "You can quickly identify what type of script is needed based on user "
            "descriptions. You excel at breaking down complex requirements into "
            "manageable components. You prefer standalone CFX scripts when no "
            "framework is specifically required."
        ),
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
    )
