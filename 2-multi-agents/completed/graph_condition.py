from strands import Agent

#Initialize an agent with agent_graph capability
from strands.multiagent import GraphBuilder

mesh_agent = Agent()
# Create specialized agents

classifier = Agent(name="classifier", system_prompt="You are an agent responsible for classification of the report request, return only Technical or Business clasification.")
technical_report = Agent(name="technical_expert", system_prompt="You are a technical expert htat focuses on providing short summary from technical perspective")
business_report = Agent(name="business_expert", system_prompt="You are a business expert that focuses on providing short summary from business perspective")

# Build the graph
builder = GraphBuilder()

# Add nodes
builder.add_node(classifier, "classifier")
builder.add_node(technical_report, "technical_report")
builder.add_node(business_report, "business_report")

def is_technical(state):
    classifier_result = state.results.get("classifier")
    if not classifier_result:
        return False
    result_text = str(classifier_result.result)
    return "technical" in result_text.lower()

def is_business(state):
    classifier_result = state.results.get("classifier")
    if not classifier_result:
        return False
    result_text = str(classifier_result.result)
    return "business" in result_text.lower()

# Add edges (dependencies)
builder.add_edge("classifier", "technical_report", condition=is_technical)
builder.add_edge("classifier", "business_report", condition=is_business)

# Set entry points (optional - will be auto-detected if not specified)
builder.set_entry_point("classifier")

# Build the graph
graph = builder.build()

print("============================================================")
print("============================================================")

#Execute task on newly built graph
result = graph("Provide report on technical aspect of working from home, outline things to consider and key risk factors")
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

print("Classifier:")
print("============================================================")
print("============================================================")
print(result.results["classifier"].result)
print("\n")

#Execute task on newly built graph
result = graph("Provide report on business impact of working from home, outline things to consider and key risk factors")
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

print("Classifier:")
print("============================================================")
print("============================================================")
print(result.results["classifier"].result)
print("\n")