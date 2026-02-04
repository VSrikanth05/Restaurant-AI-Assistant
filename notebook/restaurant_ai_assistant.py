from src.agent_setup import create_agent

agent = create_agent("data/cleaned_sales.csv")

# Example Questions
response1 = agent.run("What were the top selling items last week?")
print(response1)

response2 = agent.run("Why did sales drop on Tuesday?")
print(response2)

response3 = agent.run("Estimate how much ingredients we need next week based on last week's sales trend.")
print(response3)