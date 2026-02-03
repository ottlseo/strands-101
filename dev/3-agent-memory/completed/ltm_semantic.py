"""
LTM Semantic Memory 전략 - 사실 정보 추출 및 저장
"""
import os
from strands import Agent
from bedrock_agentcore.memory.integrations.strands.config import (
    AgentCoreMemoryConfig,
    RetrievalConfig
)
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

MEMORY_ID = os.environ.get("AGENTCORE_MEMORY_LTM_ID", "your-ltm-memory-id")

# LTM 검색 설정
retrieval_config = {
    "/facts/{actorId}": RetrievalConfig(
        top_k=5,           # 상위 5개 결과
        relevance_score=0.5  # 관련성 점수 임계값
    )
}

memory_config = AgentCoreMemoryConfig(
    memory_id=MEMORY_ID,
    session_id="ltm_session_001",
    actor_id="user_charlie",
    retrieval_config=retrieval_config
)

session_manager = AgentCoreMemorySessionManager(
    agentcore_memory_config=memory_config,
    region_name="us-west-2"
)

agent = Agent(
    system_prompt="""당신은 사용자에 대해 학습하는 어시스턴트입니다.
    대화에서 중요한 사실을 기억하고, 이전에 학습한 정보를 활용하여 응답하세요.""",
    session_manager=session_manager
)

if __name__ == "__main__":
    # 사실 정보 제공
    print("=== 사실 학습 ===")
    response1 = agent("저는 Charlie입니다. 소프트웨어 엔지니어로 일하고 있고, Python을 주로 사용해요.")
    print(f"Agent: {response1}\n")
    
    # 다른 세션에서 기억하는지 테스트
    print("=== 새 세션에서 테스트 ===")
    
    # 새 세션으로 에이전트 재생성
    new_config = AgentCoreMemoryConfig(
        memory_id=MEMORY_ID,
        session_id="ltm_session_002",  # 다른 세션
        actor_id="user_charlie",       # 같은 사용자
        retrieval_config=retrieval_config
    )
    
    new_session_manager = AgentCoreMemorySessionManager(
        agentcore_memory_config=new_config,
        region_name="us-west-2"
    )
    
    new_agent = Agent(
        system_prompt="당신은 사용자에 대해 학습하는 어시스턴트입니다.",
        session_manager=new_session_manager
    )
    
    response2 = new_agent("제가 무슨 일을 한다고 했죠?")
    print(f"Agent: {response2}")
