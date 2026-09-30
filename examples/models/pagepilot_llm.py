"""
Example of the fastest + smartest LLM for browser automation.

Setup:
1. Get your API key from https://cloud.pagepilot.com/new-api-key
2. Set environment variable: export PAGEPILOT_API_KEY="your-key"
"""

import asyncio
import os

from dotenv import load_dotenv

from pagepilot import Agent, ChatPagePilot

load_dotenv()

if not os.getenv('PAGEPILOT_API_KEY'):
	raise ValueError('PAGEPILOT_API_KEY is not set')


async def main():
	# A bare `ChatPagePilot()` gives you `bu-2-0`, the premium default (as does 'bu-latest').
	# `bu-2-0-mini-preview`, used below, is cheaper and faster per token but is in preview, so
	# you opt into it by name rather than getting it by default.
	# ChatPagePilot can also route to provider-prefixed models (e.g. 'anthropic/claude-sonnet-4-6',
	# 'openai/gpt-5.5', 'google/gemini-3-pro') through the same gateway - see
	# pagepilot_provider_models.py.
	agent = Agent(
		task='Find the number of stars of the pagepilot repo',
		llm=ChatPagePilot(model='bu-2-0-mini-preview'),
	)

	# Run the agent
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
