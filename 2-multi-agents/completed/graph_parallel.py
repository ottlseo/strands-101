from strands import Agent

#Initialize an agent with agent_graph capability
from strands.multiagent import GraphBuilder

mesh_agent = Agent()

# Create specialized agents
financial_advisor = Agent(name="financial_advisor", system_prompt="You are a financial advisor focused on cost-benefit analysis, budget implications, and ROI calculations. Engage with other experts to build comprehensive financial perspectives.")
technical_architect = Agent(name="technical_architect", system_prompt="You are a technical architect who evaluates feasibility, implementation challenges, and technical risks. Collaborate with other experts to ensure technical viability.")
market_researcher = Agent(name="market_researcher", system_prompt="You are a market researcher who analyzes market conditions, user needs, and competitive landscape. Work with other experts to validate market opportunities.")
risk_analyst = Agent(name="risk_analyst", system_prompt="You are a risk analyst who identifies potential risks, mitigation strategies, and compliance issues. Collaborate with other experts to ensure comprehensive risk assessment.")


# Build the graph
builder = GraphBuilder()

# Add nodes
builder.add_node(financial_advisor, "finance_expert")
builder.add_node(technical_architect, "tech_expert")
builder.add_node(market_researcher, "market_expert")
builder.add_node(risk_analyst, "risk_analyst")

# Add edges (dependencies)
builder.add_edge("finance_expert", "tech_expert")
builder.add_edge("finance_expert", "market_expert")
builder.add_edge("tech_expert", "risk_analyst")
builder.add_edge("market_expert", "risk_analyst")


# Set entry points (optional - will be auto-detected if not specified)
builder.set_entry_point("finance_expert")

# Build the graph
graph = builder.build()

print("============================================================")
print("============================================================")

#Execute task on newly built graph
result = graph("Our company is considering launching a new AI-powered customer service platform. Initial investment is \$2M with projected 3-year ROI of 150%. What's your financial assessment?")
print("\n")
print("============================================================")
print("============================================================")

print(f"Response: {result}")

print("=============Node execution order:==========================")
print("============================================================")

# See which nodes were executed and in what order
for node in result.execution_order:
    print(f"Executed: {node.node_id}")

print("=============Graph metrics:=================================")
print("============================================================")


# Get performance metrics
print(f"Total nodes: {result.total_nodes}")
print(f"Completed nodes: {result.completed_nodes}")
print(f"Failed nodes: {result.failed_nodes}")
print(f"Execution time: {result.execution_time}ms")
print(f"Token usage: {result.accumulated_usage}")


# Get results from specific nodes

print("Financial Advisor:")
print("============================================================")
print("============================================================")
print(result.results["finance_expert"].result)
print("\n")

print("Technical Expert:")
print("============================================================")
print("============================================================")
print(result.results["tech_expert"].result)
print("\n")

print("Market Researcher:")
print("============================================================")
print("============================================================")
print(result.results["market_expert"].result)
print("\n")
