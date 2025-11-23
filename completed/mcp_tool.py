from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uvx",
                          args=["awslabs.aws-documentation-mcp-server@latest"]
                          )
))

if __name__ == "__main__":
    user_input = "Amazon Bedrock 가격 모델이란 무엇인가요? 간결하게 설명해 주세요"

    with stdio_mcp_client:
        tools = stdio_mcp_client.list_tools_sync()
        agent = Agent(tools=tools)
        response = agent(user_input) 
