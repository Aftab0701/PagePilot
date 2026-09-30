# PagePilot

Autonomous browser automation agent powered by large language models and modern browser protocols.

PagePilot enables intelligent agents to navigate websites, inspect DOM trees, interact with page elements, submit forms, extract data, and complete multi step web workflows autonomously.

---

## Overview

PagePilot connects language models directly to browser instances via the Chrome DevTools Protocol. The engine combines vision capabilities, DOM element tree extraction, and action execution loops to perform complex tasks on the web.

### Key Capabilities

* Automated Web Navigation: Search, click, type, scroll, and handle dynamic web applications.
* Multi Model Support: Works with PagePilot models, Google Gemini, OpenAI GPT, Anthropic Claude, and local Ollama models.
* Vision and DOM Processing: Interprets visual page state and interactive DOM accessibility elements.
* Structured Output: Extract typed information validated with Pydantic models.
* Extensible Tooling: Register custom Python functions and tools that agents can execute during tasks.

---

## Quickstart

### 1. Environment Setup

PagePilot requires Python 3.11 or newer. Set up your virtual environment using uv or standard python tools:

```bash
uv venv --python 3.12
source .venv/bin/activate
uv sync
```

On Windows systems, activate your environment with:

```powershell
.\.venv\Scripts\activate
```

### 2. Configuration

Create your `.env` configuration file from the provided example:

```bash
cp .env.example .env
```

Add your API credentials:

```bash
PAGEPILOT_API_KEY=your_api_key_here
# Optional provider keys:
# OPENAI_API_KEY=your_openai_key
# GOOGLE_API_KEY=your_gemini_key
# ANTHROPIC_API_KEY=your_anthropic_key
```

---

## Usage Examples

### Basic Agent Execution

```python
import asyncio
from dotenv import load_dotenv
from pagepilot import Agent, ChatPagePilot

load_dotenv()

async def main():
    llm = ChatPagePilot()
    agent = Agent(
        task="Navigate to github.com/trending and extract the top trending repositories",
        llm=llm
    )
    history = await agent.run(max_steps=25)
    print("Execution Result:")
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
```

### Running with Alternative Models

```python
import asyncio
from dotenv import load_dotenv
from pagepilot import Agent, ChatGoogle, ChatOpenAI, ChatAnthropic

load_dotenv()

async def main():
    # Using Google Gemini
    llm = ChatGoogle(model="gemini-2.5-flash")
    
    # Or using OpenAI GPT
    # llm = ChatOpenAI(model="gpt-4o")
    
    # Or using Anthropic Claude
    # llm = ChatAnthropic(model="claude-3-7-sonnet-20250219")

    agent = Agent(
        task="Find recent news about artificial intelligence research",
        llm=llm
    )
    history = await agent.run()
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Tools Integration

You can extend agent capabilities with custom Python functions:

```python
import asyncio
from datetime import datetime, timezone
from pagepilot import Agent, ActionResult, ChatPagePilot, Tools
from dotenv import load_dotenv

load_dotenv()

tools = Tools()

@tools.action(description="Retrieve current UTC timestamp")
def get_current_time() -> ActionResult:
    now_str = datetime.now(timezone.utc).isoformat()
    return ActionResult(extracted_content=now_str)

async def main():
    agent = Agent(
        task="Check current time and summarize top tech headlines",
        llm=ChatPagePilot(),
        tools=tools
    )
    history = await agent.run()
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Command Line Interface

PagePilot includes CLI tools for diagnostics, automation workflows, and headless runs:

```powershell
# Run system and browser diagnostic check
python -m pagepilot.cli --doctor

# View all CLI commands
python -m pagepilot.cli --help
```

---

## Architecture

PagePilot follows an event driven architecture:

* Agent Orchestration (`Agent`): Manages the step loop, memory compaction, and decision execution.
* Browser Controller (`BrowserSession`): Handles browser lifecycle, CDP connection, tabs, and events.
* DOM Service (`DomService`): Serializes interactive elements, computes bounding boxes, and filters accessibility trees.
* Action Registry (`Tools`): Maps model decisions to low level browser actions like click, type, and scroll.

---

## Running Tests

Execute the automated test suite using pytest:

```powershell
python -m pytest tests/ci
```

---

## License

MIT License.
