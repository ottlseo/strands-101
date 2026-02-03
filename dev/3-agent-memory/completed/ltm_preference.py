"""
LTM User Preference 전략 - 사용자 선호도 학습
"""
import os
from strands import Agent
from bedrock_agentcore.memory.integrations.strands.config import (
    AgentCoreMemoryConfig,
    RetrievalConfig
)
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

MEMORY_ID = os.environ.get("AGENTCORE_MEMORY_LTM_ID", "your-ltm-memory-id")

retrieval_config = {
    "/preferences/{actorId}": RetrievalConfig(
        top_k=10,
        relevance_score=0.3
    )
}

memory_config = AgentCoreMemoryConfig(
    memory_id=MEMORY_ID,
    session_id="preference_session_001",
    actor_id="user_diana",
    retrieval_config=retrieval_config
)

session_manager = AgentCoreMemorySessionManager(
    agentcore_memory_config=memory_config,
    region_name="us-west-2"
)

agent = Agent(
    system_prompt="""당신은 개인화된 추천을 제공하는 어시스턴트입니다.
    사용자의 선호도를 학습하고, 맞춤형 제안을 해주세요.""",
    session_manager=session_manager
)

if __name__ == "__main__":
    # 선호도 정보 제공
    print("=== 선호도 학습 ===")
    response1 = agent("저는 한식을 좋아하고, 특히 김치찌개를 자주 먹어요. 매운 음식을 좋아해요.")
    print(f"Agent: {response1}\n")
    
    response2 = agent("영화는 SF 장르를 좋아하고, 주말에는 등산을 즐겨요.")
    print(f"Agent: {response2}\n")
    
    # 선호도 기반 추천 요청
    print("=== 추천 요청 ===")
    response3 = agent("오늘 저녁 뭐 먹을지 추천해줄래?")
    print(f"Agent: {response3}")
