"""Design Task - Designs features for FiveM scripts."""

from crewai import Task, Agent

from src.models.schemas import FeatureDesign


def create_design_task(agent: Agent) -> Task:
    """Create the feature design task.
    
    Args:
        agent: The agent to assign this task to
        
    Returns:
        Task: Configured design task with structured output
    """
    return Task(
        description="""
        Based on the requirement analysis, design comprehensive features for this FiveM script.
        
        You must:
        1. Design each core feature with clear name, description, and priority
        2. Suggest 2-4 additional AI-recommended features that would enhance the script
           - These should be practical and add real value
           - Consider quality-of-life improvements
           - Think about admin features, logging, or configuration options
        3. Define required data structures (tables, objects, etc.)
        4. List all events needed for client-server communication
           - Use proper naming convention: resourceName:eventName
        5. If database is needed, specify table structures
        
        Focus on practical, implementable features. Avoid feature bloat.
        """,
        expected_output=(
            "A comprehensive feature design including core features, AI-suggested "
            "features, required data structures, events list, and database tables."
        ),
        agent=agent,
        output_pydantic=FeatureDesign,
    )
