from strands import Agent
from strands_tools import calculator, python_repl # 참고: https://github.com/strands-agents/tools

agent = Agent(tools=[calculator, python_repl]) # tools
response = agent("What is 80/4?") # prompt

print(response)
