# FiveM CrewAI Generator

AI-powered FiveM Lua Script Generator using CrewAI

## Features

- 🤖 Multi-agent system for intelligent script generation
- 🎮 Supports ESX and QBCore frameworks
- 📝 Generates production-ready Lua code
- 🔧 Configurable and extensible architecture

## Project Structure

```
fivem-crewai-generator/
│
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── requirement_analyzer.py
│   │   ├── feature_designer.py
│   │   ├── lua_architect.py
│   │   └── code_generator.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── analyze_task.py
│   │   ├── design_task.py
│   │   ├── architect_task.py
│   │   └── generate_code_task.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── crew.py
│
├── output/
├── main.py
├── pyproject.toml
└── .env.example
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -e .
   ```
4. Copy `.env.example` to `.env` and add your Google API key:
   ```bash
   cp .env.example .env
   # Add your GOOGLE_API_KEY from https://aistudio.google.com/
   ```

## Usage

```bash
python main.py "Create a shop script for QBCore with NPC vendor, inventory integration, and configurable items"
```

Or run interactively:
```bash
python main.py
```

## Generated Output

The generator creates a complete FiveM resource folder in `output/` containing:

- `client.lua` - Client-side logic
- `server.lua` - Server-side logic
- `config.lua` - Configuration options
- `fxmanifest.lua` - Resource manifest
- `README.md` - Installation instructions

## Adding New Agents

1. Create agent file in `src/agents/new_agent.py`
2. Create task file in `src/tasks/new_task.py`
3. Update `src/crew.py`:
   - Import the new agent and task
   - Add to `_setup_agents()`
   - Add to `_setup_tasks()`
   - Add to `_get_agents()` and `_get_tasks()` lists

## Agents

| Agent | Role |
|-------|------|
| Requirement Analyzer | Analyzes user requirements and identifies script specifications |
| Feature Designer | Designs features and suggests enhancements |
| Lua Architect | Creates technical architecture and code structure |
| Code Generator | Generates production-ready Lua code |

## License

MIT
