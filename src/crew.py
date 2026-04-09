"""Crew assembly for FiveM Script Generator.

This module assembles agents and tasks into a working crew.
To add a new agent:
1. Create agent file in src/agents/
2. Create task file in src/tasks/
3. Import and add below in the marked sections
"""

from crewai import Crew, Process

# =============================================================================
# AGENT IMPORTS - Add new agent imports here
# =============================================================================
from src.agents.requirement_analyzer import create_requirement_analyzer_agent
from src.agents.feature_designer import create_feature_designer_agent
from src.agents.lua_architect import create_lua_architect_agent
from src.agents.code_generator import create_code_generator_agent

# =============================================================================
# TASK IMPORTS - Add new task imports here
# =============================================================================
from src.tasks.analyze_task import create_analyze_task
from src.tasks.design_task import create_design_task
from src.tasks.architect_task import create_architect_task
from src.tasks.generate_code_task import create_generate_code_task

from src.models.schemas import GeneratedCode


class FiveMScriptCrew:
    """FiveM Script Generator Crew.
    
    Orchestrates agents and tasks to generate FiveM Lua scripts.
    """
    
    def __init__(self, user_requirement: str) -> None:
        """Initialize the crew with user requirement.
        
        Args:
            user_requirement: The user's script requirement
        """
        self.user_requirement = user_requirement
        self._setup_agents()
        self._setup_tasks()
    
    def _setup_agents(self) -> None:
        """Setup all agents.
        
        # =====================================================================
        # ADD NEW AGENTS HERE
        # Example:
        # self.new_agent = create_new_agent()
        # =====================================================================
        """
        self.requirement_analyzer = create_requirement_analyzer_agent()
        self.feature_designer = create_feature_designer_agent()
        self.lua_architect = create_lua_architect_agent()
        self.code_generator = create_code_generator_agent()
    
    def _setup_tasks(self) -> None:
        """Setup all tasks.
        
        # =====================================================================
        # ADD NEW TASKS HERE
        # Example:
        # self.new_task = create_new_task(self.new_agent)
        # Don't forget to add to self._get_tasks() list
        # =====================================================================
        """
        self.analyze_task = create_analyze_task(
            self.requirement_analyzer,
            self.user_requirement
        )
        self.design_task = create_design_task(self.feature_designer)
        self.architect_task = create_architect_task(self.lua_architect)
        self.generate_code_task = create_generate_code_task(self.code_generator)
    
    def _get_agents(self) -> list:
        """Get list of all agents.
        
        # =====================================================================
        # ADD NEW AGENTS TO THIS LIST
        # =====================================================================
        """
        return [
            self.requirement_analyzer,
            self.feature_designer,
            self.lua_architect,
            self.code_generator,
        ]
    
    def _get_tasks(self) -> list:
        """Get list of all tasks in execution order.
        
        # =====================================================================
        # ADD NEW TASKS TO THIS LIST (order matters!)
        # =====================================================================
        """
        return [
            self.analyze_task,
            self.design_task,
            self.architect_task,
            self.generate_code_task,
        ]
    
    def create_crew(self) -> Crew:
        """Create and return the assembled crew.
        
        Returns:
            Crew: Configured CrewAI crew ready for execution
        """
        return Crew(
            agents=self._get_agents(),
            tasks=self._get_tasks(),
            process=Process.sequential,
            verbose=True,
        )
    
    def run(self) -> GeneratedCode:
        """Run the crew and return generated code.
        
        Returns:
            GeneratedCode: The generated FiveM script code
        """
        crew = self.create_crew()
        result = crew.kickoff()
        
        if isinstance(result, GeneratedCode):
            return result
        
        return self.generate_code_task.output.pydantic
