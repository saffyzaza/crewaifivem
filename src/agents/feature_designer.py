"""Feature Designer Agent - Designs features for FiveM scripts."""

from crewai import Agent

from src.config.llm_factory import create_llm


def create_feature_designer_agent() -> Agent:
    """Create the Feature Designer agent.
    
    This agent designs features based on analyzed requirements:
    - Core feature specification
    - AI-suggested additional features
    - Data structure design
    - Event system planning
    
    Returns:
        Agent: Configured Feature Designer agent
    """
    return Agent(
        role="FiveM Feature Designer",
        goal=(
            "Design comprehensive features for FiveM scripts based on analyzed "
            "requirements. Suggest additional features that enhance gameplay "
            "and user experience while maintaining code simplicity."
        ),
        backstory=(
            "You are a creative FiveM script designer who has worked on hundreds "
            "of successful roleplay servers. You understand what makes scripts "
            "engaging and user-friendly. You can anticipate features that users "
            "might not explicitly ask for but would greatly appreciate. You always "
            "consider performance implications and ensure features are practical "
            "to implement."
        ),
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
    )
