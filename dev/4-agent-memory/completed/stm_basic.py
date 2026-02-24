import os
from strands import Agent
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

# 메모리 ID (이전 섹션에서 생성한 ID)
MEMORY_ID = os.environ.get("AGENTCORE_MEMORY_ID", "your-memory-id-here")

# 세션 및 액터 설정
SESSION_ID = "workshop_session_001"
ACTOR_ID = "user_alice"

# AgentCore Memory 설정
memory_config = AgentCoreMemoryConfig(
    memory_id=MEMORY_ID,
    session_id=SESSION_ID,
    actor_id=ACTOR_ID
)

session_manager = AgentCoreMemorySessionManager(
    agentcore_memory_config=memory_config
)

agent = Agent(
    system_prompt="당신은 친절한 어시스턴트입니다. 사용자와의 대화를 기억하고 맥락에 맞게 응답하세요.",
    session_manager=session_manager
)

if __name__ == "__main__":
    # 첫 번째 대화
    print("=== 첫 번째 대화 ===")
    response1 = agent("안녕하세요! 제 이름은 Alice이고, 피자를 좋아해요.")
    
    # 두 번째 대화 - 이전 대화를 기억하는지 확인
    print("=== 두 번째 대화 ===")
    response2 = agent("제 이름이 뭐라고 했죠? 그리고 제가 좋아하는 음식은요?")
