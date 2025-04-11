# 🛠️ MCP-Tools
## Overview
MCP-Tools is a modular collection of tools and servers designed to streamline interactions with various services. This repository is built to scale, supporting multiple server modules, each offering distinct functionalities.


## 🚀 Getting Started 
1. Clone the Repository
```bash
git clone https://github.com/AxelPribadi/MCP-Tools.git
cd MCP-Tools
```

2. Install uv (if not already installed)
```bash
# For macOS using Homebrew
brew install uv

# Or via the official installation script
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Set Up and Activate the Virtual Environment
```bash
uv venv
source .venv/bin/activate (Linux/Mac)
# .venv/Scripts/activate (Windows)
```

4. Install Dependencies
```bash
uv sync
```

## 💻 Using MCP Servers
MCP-Tools is structured to support modular server folders—each serving a unique purpose. To use a specific MCP server, you'll typically navigate into its directory and follow setup instructions.

📝 Note: Each `<mcp_folder>` contains a `README.md` or other documentation that provides detailed setup and usage instructions specific to that module. The following steps outline a generic way to use any MCP server, but individual modules may require additional steps.

1. Navigate to an MCP folder
```bash
cd <mcp_folder>
# eg: cd google_calendar
```

2. Add Server to Claude
```bash
mcp install <server_name.py>
# eg: mcp install google_calendar.py
```

3. Manual Configuration (if needed or preferred)
If the server isn't installed correctly using mcp install, you can manually configure it in Claude's config file (claude_desktop_config.json):
```json
{
    "mcpServers": {
        "Server Name": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/MCP-Tools/<mcp_folder>",
                "run",
                "<server_name.py>"
            ]
        }
    }
}
```
