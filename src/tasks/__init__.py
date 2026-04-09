"""Tasks module for FiveM CrewAI Generator."""

from src.tasks.analyze_task import create_analyze_task
from src.tasks.design_task import create_design_task
from src.tasks.architect_task import create_architect_task
from src.tasks.generate_code_task import create_generate_code_task

__all__ = [
    "create_analyze_task",
    "create_design_task",
    "create_architect_task",
    "create_generate_code_task",
]
