from pagepilot import Agent, models

# available providers for this import style: openai, azure, google
agent = Agent(task='Find founders of pagepilot', llm=models.azure_gpt_4_1_mini)

agent.run_sync()
