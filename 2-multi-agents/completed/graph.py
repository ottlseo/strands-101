from strands import Agent

#Initialize an agent with agent_graph capability
from strands.multiagent import GraphBuilder

# Create specialized agents
coordinator = Agent(name="coordinator", system_prompt="You are a research team leader coordinating specialists. Provide a short analysis, no need for follow ups")
analyst = Agent(name="data_analyst", system_prompt="You are a data analyst specializing in statistical analysis. Provide a short analysis, no need for follow ups")
domain_expert = Agent(name="domain_expert", system_prompt="You are a domain expert with deep subject knowledge. Provide a short analysis, no need for follow ups")

# Build the graph
builder = GraphBuilder()

# Add nodes
builder.add_node(coordinator, "team_lead")
builder.add_node(analyst, "analyst")
builder.add_node(domain_expert, "expert")

# Add edges (dependencies)
builder.add_edge("team_lead", "analyst")
builder.add_edge("team_lead", "expert")

# Set entry points (optional - will be auto-detected if not specified)
builder.set_entry_point("team_lead")

# Build the graph
graph = builder.build()

#Execute task on newly built graph
result = graph("Analyze the impact of remote work on employee productivity.Provide a short analysis, no need for follow ups")
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
print("\n")
print("=============Expert node results only:======================")
print("============================================================")
print(result.results["expert"].result)