"""Run the Rust-backed Browser Use Agent.

Set PAGEPILOT_TERMINAL_BINARY when the terminal binary is not on PATH.
Set BU_CDP_URL or PAGEPILOT_CDP_URL to attach to a remote Browser Use cloud browser.
"""

import asyncio
import os

from pagepilot.beta import Agent, BrowserSession, ChatPagePilot

# from pagepilot.beta import ChatOpenAI  # ChatOpenAI(model='gpt-5.5')
# from pagepilot.beta import ChatGoogle  # ChatGoogle(model='gemini-3.1-pro-preview')
# from pagepilot.beta import ChatAnthropic  # ChatAnthropic(model='claude-opus-4-8')


async def main() -> None:
	cdp_url = os.environ.get('BU_CDP_URL') or os.environ.get('PAGEPILOT_CDP_URL')
	browser_session = BrowserSession(cdp_url=cdp_url) if cdp_url else None
	task = os.environ.get('BU_TASK', 'Open https://example.com and report the page title.')
	max_steps = int(os.environ.get('BU_MAX_STEPS', '20'))

	agent = Agent(
		task=task,
		llm=ChatPagePilot(model='openai/gpt-5.5'),
		# llm=ChatPagePilot(),  # Browser Use's own optimized model (bu-2-0)
		# llm=ChatOpenAI(model='gpt-5.5'),
		# llm=ChatGoogle(model='gemini-3.1-pro-preview'),
		# llm=ChatAnthropic(model='claude-opus-4-8'),  # Sonnet also works well.
		browser_session=browser_session,
	)
	history = await agent.run(max_steps=max_steps)
	print(history.final_result() or '(no final result)')


if __name__ == '__main__':
	asyncio.run(main())
