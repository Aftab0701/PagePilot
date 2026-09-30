"""
Setup:
1. Get your API key from https://cloud.pagepilot.com/new-api-key
2. Set environment variable: export PAGEPILOT_API_KEY="your-key"
"""

import asyncio
import os
import sys

# Add the parent directory to the path so we can import pagepilot
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from pagepilot import Agent, ChatPagePilot


async def main():
	llm = ChatPagePilot(model='bu-2-0-mini-preview')
	task = "Search Google for 'what is browser automation' and tell me the top 3 results"
	agent = Agent(task=task, llm=llm)
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
