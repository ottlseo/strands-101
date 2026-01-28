from strands import Agent
from strands_tools import calculator, current_time, python_repl # 참고: https://github.com/strands-agents/tools

agent = Agent(tools=[calculator, current_time, python_repl]) # tools
response = agent("80 / 4 * 5 의 제곱근은?") # prompt
