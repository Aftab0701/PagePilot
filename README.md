<img width="2172" height="724" alt="pagepilot" src="https://github.com/user-attachments/assets/363d4307-1607-4946-bead-c64530d0b197" />



# PagePilot: Autonomous AI Browser Automation Framework

The open source Python engine for autonomous web navigation, intelligent data extraction, form filling, and modern browser automation powered by Large Language Models and the Chrome DevTools Protocol.

PagePilot transforms language models into autonomous web agents that can control Chromium browsers, parse interactive DOM trees, interact with complex dynamic web applications, and execute multi step workflows from plain language prompts.

---

## Why PagePilot?

Traditional web automation tools like Playwright, Selenium, and Puppeteer require manually maintaining fragile CSS selectors, XPath strings, and rigid wait timeouts. Whenever a website updates its layout, classic automation scripts break.

PagePilot provides a self healing alternative:
* It reads the interactive accessibility tree and visual screen state.
* It plans and executes actions dynamically based on high level goals.
* It adapts when UI elements shift or change layout.
* It batches multiple actions per step to minimize latency and token costs.

| Feature | Legacy Scripting (Playwright / Selenium) | PagePilot AI Automation |
| :--- | :--- | :--- |
| Selector Maintenance | Manual CSS and XPath strings (breaks easily) | Zero manual selectors, autonomous DOM understanding |
| Workflow Definition | Rigid procedural code | Plain English task prompts |
| Form Filling | Explicit element click and type commands | Autonomous multi action batching in a single turn |
| Dynamic Layouts | Fails on A/B tests and redesigns | Self healing reasoning that adapts to UI updates |
| Data Extraction | Manual regex and HTML parsing | Typed Pydantic v2 structured schemas |
| Supported Models | None (manual code only) | Gemini, OpenAI, Claude, and local Ollama models |

---

## Core Capabilities

* Autonomous Web Navigation: Search, click, type, scroll, handle pagination, and manage browser tabs.
* Multi Action Execution: Batches sequential interactions (such as multi field form submission) into a single step for low latency and token efficiency.
* Token Cost Optimization: Strips non interactive styling and script tags, generating lightweight accessibility trees rather than raw HTML dumps.
* Vision and Layout Awareness: Supports screenshot analysis for visual validation alongside DOM element inspection.
* Type Safe Extraction: Validates extracted data into strict Pydantic schemas for reliable API pipelines.
* Local First Automation: Compatible with local Ollama models (Qwen, Llama, Mistral) for private, zero cost offline automation.

---

## Installation

PagePilot requires Python 3.11 or newer. We recommend using `uv` for fast dependency management:

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e .
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\activate
uv pip install -e .
```

---

## Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Set your preferred provider API key:

```bash
PAGEPILOT_API_KEY=your_key_here
# Optional alternatives:
# OPENAI_API_KEY=your_key_here
# GOOGLE_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
```

---

## Quickstart Guide

### 1. Basic Autonomous Task

```python
import asyncio
from dotenv import load_dotenv
from pagepilot import Agent, ChatBrowserUse

load_dotenv()

async def main():
    agent = Agent(
        task="Go to github.com/trending, find the top 3 trending repositories, and extract their stars and descriptions.",
        llm=ChatBrowserUse()
    )
    history = await agent.run(max_steps=25)
    print("Result:")
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Multi Model Support (Gemini, GPT, Claude, Ollama)

```python
import asyncio
from dotenv import load_dotenv
from pagepilot import Agent, ChatGoogle, ChatOpenAI, ChatAnthropic, ChatOllama

load_dotenv()

async def main():
    # Google Gemini
    llm = ChatGoogle(model="gemini-2.5-flash")
    
    # Or OpenAI GPT
    # llm = ChatOpenAI(model="gpt-4o")
    
    # Or Anthropic Claude
    # llm = ChatAnthropic(model="claude-3-7-sonnet-20250219")
    
    # Or Local Ollama
    # llm = ChatOllama(model="qwen2.5:latest")

    agent = Agent(
        task="Search arxiv.org for the latest research papers on autonomous AI agents and summarize their findings.",
        llm=llm
    )
    history = await agent.run()
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Structured Data Extraction with Pydantic

```python
import asyncio
from pydantic import BaseModel, Field
from pagepilot import Agent, ChatGoogle
from dotenv import load_dotenv

load_dotenv()

class ProductInfo(BaseModel):
    title: str = Field(description="Name of the product")
    price: str = Field(description="Current listed price")
    rating: str = Field(description="Customer review rating")

async def main():
    agent = Agent(
        task="Extract pricing and rating details for the top recommended laptop on the store page.",
        llm=ChatGoogle(model="gemini-2.5-flash"),
        output_model_schema=ProductInfo
    )
    history = await agent.run()
    print("Structured Output:", history.structured_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Extending Agents with Custom Tools

```python
import asyncio
from datetime import datetime, timezone
from pagepilot import Agent, ActionResult, Tools, ChatGoogle
from dotenv import load_dotenv

load_dotenv()

tools = Tools()

@tools.action(description="Get the current UTC timestamp")
def get_timestamp() -> ActionResult:
    return ActionResult(extracted_content=datetime.now(timezone.utc).isoformat())

async def main():
    agent = Agent(
        task="Check current time using get_timestamp and search for today's top tech news.",
        llm=ChatGoogle(model="gemini-2.5-flash"),
        tools=tools
    )
    history = await agent.run()
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Command Line Interface

PagePilot includes CLI tools for quick verification, diagnostics, and headless execution:

```powershell
# Run environment and browser diagnostic check
python -m pagepilot.cli --doctor

# View CLI commands
python -m pagepilot.cli --help
```

---

## Common Use Cases

* Automated Web Scraping: Extract data from single page applications, infinite scroll feeds, and login gated portals.
* QA and Synthetic Testing: Test critical user journeys (signup, checkout, onboarding) without writing brittle test scripts.
* Business Process Automation (RPA): Complete repetitive back office web tasks across legacy ERP and CRM dashboards.
* Competitive Intelligence: Track dynamic pricing, inventory levels, and product availability automatically.

---

## Running the Test Suite

```powershell
python -m pytest tests/ci
```

---

## License

MIT License.
