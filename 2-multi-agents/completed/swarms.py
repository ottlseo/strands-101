import logging
from strands import Agent
from strands.multiagent import Swarm
from strands.models import BedrockModel
from strands_tools import file_write

logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    max_tokens=64000
)

# Create specialized agents with different expertise
research_agent = Agent(
    name="research_agent",
    model=model,
    system_prompt="""You are a Research Agent specializing in gathering and analyzing information.
Your role in the swarm is to provide factual information and research insights on the topic.
You should focus on providing accurate data and identifying key aspects of the problem.

IMPORTANT: After completing your research, you MUST save your findings to a file named 'research.md' using the file_write tool before handing off to another agent.
When you need creative input or critical analysis, use handoff_to_agent to transfer to the appropriate specialist.""",
    tools=[file_write]
)

creative_agent = Agent(
    name="creative_agent",
    model=model,
    system_prompt="""You are a Creative Agent specializing in generating innovative solutions.
Your role in the swarm is to think outside the box and propose creative approaches.
You should build upon information from other agents while adding your unique creative perspective.

IMPORTANT: After completing your creative proposal, you MUST save it to a file named 'creative.md' using the file_write tool before handing off to another agent.
When you need research data or critical evaluation, handoff to the appropriate agent.""",
    tools=[file_write]
)

critical_agent = Agent(
    name="critical_agent",
    model=model,
    system_prompt="""You are a Critical Agent specializing in analyzing proposals and finding flaws.
Your role in the swarm is to evaluate solutions proposed by other agents and identify potential issues.
You should carefully examine proposed solutions, find weaknesses or opportunities for improvement.

IMPORTANT: After completing your analysis, you MUST save it to a file named 'critical.md' using the file_write tool before handing off to another agent.
When you need additional research or creative alternatives, handoff to the appropriate agent.""",
    tools=[file_write]
)

summarizer_agent = Agent(
    name="summarizer_agent",
    model=model,
    system_prompt="""You are a Summarizer Agent specializing in synthesizing information from multiple sources.
Your role in the swarm is to take inputs from other agents and create comprehensive, well-structured summaries.
You should integrate insights from research, creative, and critical perspectives into a cohesive final result.

IMPORTANT: After creating your summary, you MUST save it to a file named 'summarizer.md' using the file_write tool.""",
    tools=[file_write]
)

# Create a swarm with these agents
swarm = Swarm(
    [research_agent, creative_agent, critical_agent, summarizer_agent],
    max_handoffs=20,
    max_iterations=20,
    execution_timeout=900.0,  # 15 minutes
    node_timeout=300.0,       # 5 minutes per agent
    repetitive_handoff_detection_window=8,  # There must be >= 3 unique agents in the last 8 handoffs
    repetitive_handoff_min_unique_agents=3
)

# Execute the swarm on a task
result = swarm("해외 MZ세대와 함께 대한민국 서울을 여행하는 프로그램을 구상중입니다. 3일 여행의 스케줄을 짜주세요. 최종 결과는 travel_plan.md 파일에 한국어로 저장하세요. ")

# Access the final result
print(f"Status: {result.status}")
print(f"Node history: {[node.node_id for node in result.node_history]}")
print(f"Final result: {result.results}")

# Get performance metrics
print(f"Total iterations: {result.execution_count}")
print(f"Execution time: {result.execution_time}ms")
print(f"Token usage: {result.accumulated_usage}")
