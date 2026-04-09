"""Pydantic V2 schemas for structured output."""

from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field


class FrameworkType(str, Enum):
    """Supported FiveM frameworks."""
    CFX_DEFAULT = "cfx_default"
    ESX = "esx"
    QBCORE = "qbcore"


class Feature(BaseModel):
    """Single feature definition."""
    name: str = Field(..., description="Feature name")
    description: str = Field(..., description="Feature description")
    priority: str = Field(default="medium", description="Feature priority: low, medium, high")
    dependencies: List[str] = Field(default_factory=list, description="List of dependent features")


class RequirementAnalysis(BaseModel):
    """Output schema for requirement analysis task."""
    script_name: str = Field(..., description="Name of the FiveM script")
    script_type: str = Field(..., description="Type of script (job, shop, system, etc.)")
    framework: FrameworkType = Field(..., description="Target framework (ESX or QBCore)")
    core_features: List[str] = Field(..., description="List of core features identified")
    target_audience: str = Field(..., description="Target audience for the script")
    complexity_level: str = Field(..., description="Complexity level: simple, medium, complex")
    raw_requirements: str = Field(..., description="Original requirements from user")


class FeatureDesign(BaseModel):
    """Output schema for feature design task."""
    features: List[Feature] = Field(..., description="List of designed features")
    ai_suggested_features: List[Feature] = Field(
        default_factory=list,
        description="Additional features suggested by AI"
    )
    data_structures: List[str] = Field(..., description="Required data structures")
    events_needed: List[str] = Field(..., description="List of events needed")
    database_tables: List[str] = Field(default_factory=list, description="Database tables if needed")


class ScriptFile(BaseModel):
    """Single script file definition."""
    filename: str = Field(..., description="File name (e.g., client.lua)")
    purpose: str = Field(..., description="Purpose of this file")
    functions: List[str] = Field(..., description="List of functions in this file")
    events: List[str] = Field(..., description="List of events in this file")


class ScriptArchitecture(BaseModel):
    """Output schema for Lua architecture task."""
    resource_name: str = Field(..., description="FiveM resource name")
    framework: FrameworkType = Field(..., description="Target framework")
    files: List[ScriptFile] = Field(..., description="List of script files")
    shared_variables: List[str] = Field(default_factory=list, description="Shared variables across files")
    config_options: List[str] = Field(..., description="Configuration options")
    dependencies: List[str] = Field(default_factory=list, description="External dependencies")


class FiveMScript(BaseModel):
    """Single FiveM script file content."""
    filename: str = Field(..., description="File name")
    content: str = Field(..., description="Lua code content")


class GeneratedCode(BaseModel):
    """Output schema for code generation task."""
    resource_name: str = Field(..., description="FiveM resource name")
    framework: FrameworkType = Field(..., description="Framework used")
    client_lua: str = Field(..., description="Content of client.lua")
    server_lua: str = Field(..., description="Content of server.lua")
    config_lua: str = Field(..., description="Content of config.lua")
    fxmanifest_lua: str = Field(..., description="Content of fxmanifest.lua")
    additional_files: List[FiveMScript] = Field(
        default_factory=list,
        description="Any additional Lua files"
    )
    installation_notes: Optional[str] = Field(
        default=None,
        description="Installation instructions"
    )
