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

    agent = Agent(tools=[stdio_mcp_client])
    response = agent(user_input) 
