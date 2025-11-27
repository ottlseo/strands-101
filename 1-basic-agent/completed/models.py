from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator

bedrock_model = BedrockModel(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    additional_request_fields={
        "anthropic_beta": [ "interleaved-thinking-2025-05-14" ], # interleaved thinking(인터리브드 씽킹)은 Claude 4 및 그 기반 AI 에이전트(예: Strands Agent)가 툴을 사용하는 과정에서 인간 전문가처럼 "사고와 행동을 번갈아"가며 진행하는 고급 에이전트 추론 모드입니다.
        "thinking": { "type": "enabled", "budget_tokens": 8000 },
    }
)
agent = Agent(
    # model=bedrock_model,
    tools=[calculator]
    )

if __name__ == "__main__":
    user_input = "Amazon Bedrock이 뭐야?"

    response = agent(user_input) 
