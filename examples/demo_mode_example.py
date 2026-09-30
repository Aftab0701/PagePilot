import asyncio

from pagepilot import Agent, ChatPagePilot


async def main() -> None:
	agent = Agent(
		task='Please find the latest commit on pagepilot/pagepilot repo and tell me the commit message. Please summarize what it is about.',
		llm=ChatPagePilot(model='bu-2-0-mini-preview'),
		demo_mode=True,
	)
	await agent.run(max_steps=5)


if __name__ == '__main__':
	asyncio.run(main())
