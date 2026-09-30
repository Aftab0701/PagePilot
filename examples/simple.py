"""
Setup:
1. Get your API key from https://cloud.pagepilot.com/new-api-key
2. Set environment variable: export PAGEPILOT_API_KEY="your-key"
"""

from dotenv import load_dotenv

from pagepilot import Agent, ChatPagePilot

load_dotenv()

agent = Agent(
	task='Find the number of stars of the following repos: pagepilot, playwright, stagehand, react, nextjs',
	llm=ChatPagePilot(model='bu-2-0-mini-preview'),
)
agent.run_sync()
