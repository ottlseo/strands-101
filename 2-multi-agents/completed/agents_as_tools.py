import os

from strands import Agent, tool
from strands_tools import file_write

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
        # Strands agents를 사용하면 특화된 에이전트를 쉽게 만들 수 있습니다
        research_agent = Agent(
            system_prompt="""You are a specialized research assistant. 
            Focus only on providing factual, well-sourced information in response to research questions.
            Always cite your sources when possible.""",
        )

        # 에이전트를 호출하고 응답을 반환합니다
        response = research_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"
    
@tool
def product_recommendation_assistant(query: str) -> str:
    """
    Handle product recommendation queries by suggesting appropriate products.

    Args:
        query: A product inquiry with user preferences

    Returns:
        Personalized product recommendations with reasoning
    """
    try:
        product_agent = Agent(
            model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            system_prompt="""You are a specialized product recommendation assistant.
            Provide personalized product suggestions based on user preferences. Always cite your sources.""",
        )
        # Call the agent and return its response
        response = product_agent(query)

        return str(response)
    except Exception as e:
        return f"Error in product recommendation: {str(e)}"

@tool
def trip_planning_assistant(query: str) -> str:
    """
    Create travel itineraries and provide travel advice.

    Args:
        query: A travel planning request with destination and preferences

    Returns:
        A detailed travel itinerary or travel advice
    """
    try:
        travel_agent = Agent(
            model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",  # Optional: Specify the model ID
            system_prompt="""You are a specialized travel planning assistant.
            Create detailed travel itineraries based on user preferences.""",
        )
        # Call the agent and return its response
        response = travel_agent(query)

        return str(response)
    except Exception as e:
        return f"Error in trip planning: {str(e)}"
    

if __name__ == "__main__":

    MAIN_SYSTEM_PROMPT = """
    당신은 쿼리를 특화된 에이전트로 라우팅하는 보조(Assistant)입니다:
    - 연구 질문 및 사실적 정보를 위해 → research_assistant 도구를 사용하세요
    - 제품 추천 및 쇼핑 조언을 위해 → product_recommendation_assistant 도구를 사용하세요
    - 여행 계획 및 일정을 위해 → trip_planning_assistant 도구를 사용하세요
    - 특화된 지식이 필요하지 않은 간단한 질문을 위해 → 직접 답변하세요

    항상 사용자의 쿼리에 따라 가장 적절한 도구를 선택하세요.
    """

    # Strands Agents를 사용하면 에이전트 도구를 쉽게 통합할 수 있습니다
    orchestrator = Agent(
        system_prompt=MAIN_SYSTEM_PROMPT,
        tools=[
            research_assistant,
            product_recommendation_assistant,
            trip_planning_assistant,
            file_write,
        ],
    )
    # customer_query = (
    #     "I'm looking for hiking boots. Write the final response to current directory."
    # )
    os.environ["DEV"] = "true"
    # # 오케스트레이터는 자동으로 이것이 여러 특화된 에이전트가 필요하다고 판단합니다
    # response = orchestrator(customer_query)

    customer_query = "스페인 국가에 대해서 리서치 좀 해줄 수 있니? 그리고 부모님과 그곳으로 7일 여행 가려고 하는데 계획 세우는 걸 좀 도와줘. 너가 세운 계획은 plan.md 파일로 저장해줘. "

    response = orchestrator(customer_query)
