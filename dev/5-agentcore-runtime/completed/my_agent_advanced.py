from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool

app = BedrockAgentCoreApp()

# 전문 에이전트 1: 연구 어시스턴트
@tool
def research_assistant(query: str) -> str:
    """
    연구 관련 쿼리를 처리하고 응답합니다.

    Args:
        query: 사실적 정보가 필요한 연구 질문

    Returns:
        인용이 포함된 상세한 연구 답변
    """
    try:
        research_agent = Agent(
            system_prompt="""당신은 전문 리서치 어시스턴트입니다.
            연구 질문에 대해 사실적이고 출처가 명확한 정보만 제공하는 데 집중하세요.
            가능한 한 항상 출처를 인용하세요.""",
        )
        response = research_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"


# 전문 에이전트 2: 제품 추천 어시스턴트
@tool
def product_recommendation_assistant(query: str) -> str:
    """
    적절한 제품을 제안하여 제품 추천 쿼리를 처리합니다.

    Args:
        query: 사용자 선호도가 포함된 제품 문의

    Returns:
        추론이 포함된 개인화된 제품 추천
    """
    try:
        product_agent = Agent(
            system_prompt="""당신은 전문 제품 추천 어시스턴트입니다.
            사용자의 선호도를 바탕으로 개인화된 제품 제안을 제공하세요.
            항상 추천 이유를 명확히 설명하세요.""",
        )
        response = product_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in product recommendation: {str(e)}"


# 전문 에이전트 3: 여행 계획 어시스턴트
@tool
def trip_planning_assistant(query: str) -> str:
    """
    여행 일정을 작성하고 여행 조언을 제공합니다.

    Args:
        query: 목적지와 선호도가 포함된 여행 계획 요청

    Returns:
        상세한 여행 일정 또는 여행 조언
    """
    try:
        travel_agent = Agent(
            system_prompt="""당신은 전문 여행 계획 어시스턴트입니다.
            사용자의 선호도를 바탕으로 상세한 여행 일정을 작성하세요.
            예산, 교통, 숙박, 관광지 등을 포함한 실용적인 계획을 제공하세요.""",
        )
        response = travel_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in trip planning: {str(e)}"


# 전문 에이전트 4: 데이터 분석 어시스턴트
@tool
def data_analysis_assistant(query: str) -> str:
    """
    데이터 분석 및 통계 관련 질문을 처리합니다.

    Args:
        query: 데이터 분석, 통계, 시각화 관련 질문

    Returns:
        분석 결과 및 인사이트
    """
    try:
        analysis_agent = Agent(
            system_prompt="""당신은 전문 데이터 분석가입니다.
            데이터 분석, 통계, 시각화에 대한 전문적인 조언을 제공하세요.
            수치와 패턴을 명확히 설명하고, 실행 가능한 인사이트를 제공하세요.""",
        )
        response = analysis_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in data analysis: {str(e)}"


# 전문 에이전트 5: 코딩 어시스턴트
@tool
def coding_assistant(query: str) -> str:
    """
    프로그래밍 및 코딩 관련 질문을 처리합니다.

    Args:
        query: 프로그래밍, 디버깅, 코드 리뷰 관련 질문

    Returns:
        코드 예시와 설명이 포함된 답변
    """
    try:
        coding_agent = Agent(
            system_prompt="""당신은 전문 프로그래밍 어시스턴트입니다.
            코드 작성, 디버깅, 최적화, 베스트 프랙티스에 대한 조언을 제공하세요.
            명확한 코드 예시와 설명을 함께 제공하세요.""",
        )
        response = coding_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in coding assistant: {str(e)}"


# 메인 오케스트레이터 시스템 프롬프트
MAIN_SYSTEM_PROMPT = """
당신은 쿼리를 특화된 에이전트로 라우팅하는 멀티 에이전트 오케스트레이터입니다.

사용 가능한 전문 에이전트:
- research_assistant: 연구 질문 및 사실적 정보 조사
- product_recommendation_assistant: 제품 추천 및 쇼핑 조언
- trip_planning_assistant: 여행 계획 및 일정 작성
- data_analysis_assistant: 데이터 분석, 통계, 시각화
- coding_assistant: 프로그래밍, 디버깅, 코드 리뷰

작업 방식:
1. 사용자의 쿼리를 분석하여 가장 적절한 전문 에이전트를 선택하세요
2. 필요시 여러 에이전트를 순차적으로 호출할 수 있습니다
3. 복잡한 요청의 경우 여러 에이전트의 결과를 조합하세요
4. 간단한 질문은 직접 답변하세요

항상 사용자의 요구사항에 맞는 최적의 에이전트를 선택하고,
명확하고 유용한 답변을 제공하세요.
"""


@app.entrypoint
def invoke(payload):
    """멀티 에이전트 오케스트레이터 엔트리포인트"""
    user_message = payload.get("prompt", "안녕하세요!")

    orchestrator = Agent(
        system_prompt=MAIN_SYSTEM_PROMPT,
        tools=[
            research_assistant,
            product_recommendation_assistant,
            trip_planning_assistant,
            data_analysis_assistant,
            coding_assistant,
        ],
    )

    # 오케스트레이터에 쿼리 전달
    result = orchestrator(user_message)

    return {
        "result": result.message,
        "agent_type": "multi-agent-orchestrator",
    }


if __name__ == "__main__":
    app.run()
