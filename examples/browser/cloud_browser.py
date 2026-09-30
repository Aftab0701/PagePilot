"""
Examples of using PagePilot cloud browser service.

Prerequisites:
1. Set PAGEPILOT_API_KEY environment variable
2. Active subscription at https://cloud.pagepilot.com
"""

import asyncio

from dotenv import load_dotenv

from pagepilot import Agent, Browser, ChatPagePilot

load_dotenv()


async def basic():
	"""Simplest usage - just pass cloud params directly."""
	browser = Browser(use_cloud=True)

	agent = Agent(
		task='Go to github.com/pagepilot/pagepilot and tell me the star count',
		llm=ChatPagePilot(model='bu-2-0-mini-preview'),
		browser=browser,
	)

	result = await agent.run()
	print(f'Result: {result}')


async def full_config():
	"""Full cloud configuration with specific profile."""
	browser = Browser(
		# cloud_profile_id='21182245-590f-4712-8888-9611651a024c',
		cloud_proxy_country_code='jp',
		cloud_timeout=60,
	)

	agent = Agent(
		task='go and check my ip address and the location',
		llm=ChatPagePilot(model='bu-2-0-mini-preview'),
		browser=browser,
	)

	result = await agent.run()
	print(f'Result: {result}')


async def main():
	try:
		# await basic()
		await full_config()
	except Exception as e:
		print(f'Error: {e}')


if __name__ == '__main__':
	asyncio.run(main())
