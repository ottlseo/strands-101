---
title : "🤝 멀티 에이전트 시스템 실습"
weight : 33
---

이번 실습에서는 Strands SDK의 멀티 에이전트 패턴을 사용하여 여러 에이전트가 협업하는 시스템을 구축하는 방법을 학습합니다.

## 실습 소개

단일 에이전트로는 해결하기 어려운 복잡한 문제를 여러 전문 에이전트가 협업하여 해결하는 방법을 알아봅니다.
`2-multi-agents/completed/` 디렉토리의 완성된 코드를 같은 디렉토리의 `labs/` 폴더 내의 빈 파일에 직접 작성하면서, Strands SDK의 멀티 에이전트 패턴을 이해합니다.

**학습 목표:**
- Agents-as-Tools 패턴: 에이전트를 다른 에이전트의 도구로 활용
- Swarm 패턴: 여러 에이전트의 자율적 협업
- Graph 패턴: 그래프 기반 워크플로우 구축 (기본/조건부/병렬)

---

## 1. Agents-as-Tools 패턴

Agents-as-Tools 패턴은 전문화된 에이전트를 도구로 래핑하여 다른 에이전트가 필요에 따라 호출할 수 있게 하는 방식입니다.

**1-1.** `2-multi-agents/labs/agents_as_tools.py` 파일을 엽니다.

**1-2.** 필요한 라이브러리를 import 합니다.

```py
import os

from strands import Agent, tool
from strands_tools import file_write
```

**1-3.** 첫 번째 전문 에이전트를 `@tool`로 래핑합니다.

연구 관련 질문에 특화된 에이전트를 도구로 만듭니다.

```py
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
            system_prompt="""You are a specialized research assistant.
            Focus only on providing factual, well-sourced information in response to research questions.
            Always cite your sources when possible.""",
        )
        response = research_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"
```

`@tool` 데코레이터로 감싸진 함수 내부에서 전문 에이전트를 생성하고 호출합니다. 이렇게 하면 에이전트가 하나의 도구처럼 동작합니다.

**1-4.** 제품 추천 에이전트를 도구로 추가합니다.

```py
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
        response = product_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in product recommendation: {str(e)}"
```

**1-5.** 여행 계획 에이전트를 도구로 추가합니다.

```py
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
            model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            system_prompt="""You are a specialized travel planning assistant.
            Create detailed travel itineraries based on user preferences.""",
        )
        response = travel_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in trip planning: {str(e)}"
```

**1-6.** 오케스트레이터 에이전트를 생성합니다.

```py
if __name__ == "__main__":

    MAIN_SYSTEM_PROMPT = """
    당신은 쿼리를 특화된 에이전트로 라우팅하는 보조(Assistant)입니다:
    - 연구 질문 및 사실적 정보를 위해 → research_assistant 도구를 사용하세요
    - 제품 추천 및 쇼핑 조언을 위해 → product_recommendation_assistant 도구를 사용하세요
    - 여행 계획 및 일정을 위해 → trip_planning_assistant 도구를 사용하세요
    - 특화된 지식이 필요하지 않은 간단한 질문을 위해 → 직접 답변하세요

    항상 사용자의 쿼리에 따라 가장 적절한 도구를 선택하세요.
    """

    orchestrator = Agent(
        system_prompt=MAIN_SYSTEM_PROMPT,
        tools=[
            research_assistant,
            product_recommendation_assistant,
            trip_planning_assistant,
            file_write,
        ],
    )
```

오케스트레이터는 사용자 요청을 분석하여 적절한 전문 에이전트(도구)를 선택하고 호출합니다.

**1-7.** 에이전트를 실행합니다.

```py
    os.environ["DEV"] = "true"
    customer_query = "스페인 국가에 대해서 리서치 좀 해줄 수 있니? 그리고 부모님과 그곳으로 7일 여행 가려고 하는데 계획 세우는 걸 좀 도와줘. 너가 세운 계획은 plan.md 파일로 저장해줘."

    response = orchestrator(customer_query)
```

**1-8.** 터미널에서 실행하여 결과를 확인합니다:

```bash
uv run 2-multi-agents/labs/agents_as_tools.py
```

오케스트레이터가 질문을 분석하여 먼저 `research_assistant`를 호출하고, 그 다음 `trip_planning_assistant`를 호출하여 여행 계획을 세우는 것을 확인할 수 있습니다.

::::alert{header="📤 Agents-as-Tools 패턴 알아보기"}

Agents-as-Tools 패턴의 핵심은 **에이전트를 도구로 래핑**하는 것입니다.

방금 우리가 Tool로 정의했던 `research_assistant`, `product_recommendation_assistant`, `trip_planning_assistant`는 각각 내부에 전문화된 에이전트를 가지고 있습니다. 이 에이전트들은:

1. 오케스트레이터로부터 특정 요청을 받으면
2. 에이전트처럼 자율적으로 방법을 판단하고
3. 필요한 경우 자신만의 도구를 사용하여 작업을 수행합니다

:::expand{header="계층 구조 시각화" defaultExpanded=true}
```
                        Orchestrator (최상위 - 라우터)
                                   |
        ┌──────────────────────────┼────────────────────────────┐
        ↓                          ↓                            ↓
   research_assistant    product_recommendation    trip_planning_assistant
   (에이전트이자 도구)         (에이전트이자 도구)           (에이전트이자 도구)
        |                          |                            |
    [내부 Agent]               [내부 Agent]                 [내부 Agent]
```
:::

이처럼 Strands SDK는 에이전트를 도구로 래핑하여 **계층적 멀티 에이전트 시스템**을 손쉽게 구현할 수 있게 합니다.

더 자세한 내용은 [공식 문서](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agents-as-tools/)를 참고하세요.
::::

---

## 2. Swarm 패턴

Swarm 패턴은 여러 전문 에이전트가 자율적으로 협업하며 작업을 handoff(전달)하는 방식입니다. 에이전트들이 서로 필요에 따라 작업을 넘겨주며 최종 결과를 만들어냅니다.

**2-1.** `2-multi-agents/labs/swarms.py` 파일을 엽니다.

**2-2.** 필요한 라이브러리를 import 합니다.

```py
import logging
from strands import Agent
from strands.multiagent import Swarm
from strands.models import BedrockModel
from strands_tools import file_write

logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)
```

**2-3.** 공통 모델을 설정합니다.

```py
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    max_tokens=64000
)
```

**2-4.** 첫 번째 전문 에이전트를 생성합니다.

```py
research_agent = Agent(
    name="research_agent",
    model=model,
    system_prompt="""You are a Research Agent specializing in gathering and analyzing information.
Your role in the swarm is to provide factual information and research insights on the topic.
You should focus on providing accurate data and identifying key aspects of the problem.

IMPORTANT: After completing your research, you MUST save your findings to a file named 'research.md' using the file_write tool before handing off to another agent.
When you need creative input or critical analysis, use handoff_to_agent to transfer to the appropriate specialist.""",
    tools=[file_write]
)
```

Swarm에서는 각 에이전트가 `handoff_to_agent` 기능을 사용하여 다른 에이전트에게 작업을 전달할 수 있습니다.

**2-5.** 나머지 전문 에이전트들을 생성합니다.

```py
creative_agent = Agent(
    name="creative_agent",
    model=model,
    system_prompt="""You are a Creative Agent specializing in generating innovative solutions.
Your role in the swarm is to think outside the box and propose creative approaches.
You should build upon information from other agents while adding your unique creative perspective.

IMPORTANT: After completing your creative proposal, you MUST save it to a file named 'creative.md' using the file_write tool before handing off to another agent.
When you need research data or critical evaluation, handoff to the appropriate agent.""",
    tools=[file_write]
)

critical_agent = Agent(
    name="critical_agent",
    model=model,
    system_prompt="""You are a Critical Agent specializing in analyzing proposals and finding flaws.
Your role in the swarm is to evaluate solutions proposed by other agents and identify potential issues.
You should carefully examine proposed solutions, find weaknesses or opportunities for improvement.

IMPORTANT: After completing your analysis, you MUST save it to a file named 'critical.md' using the file_write tool before handing off to another agent.
When you need additional research or creative alternatives, handoff to the appropriate agent.""",
    tools=[file_write]
)

summarizer_agent = Agent(
    name="summarizer_agent",
    model=model,
    system_prompt="""You are a Summarizer Agent specializing in synthesizing information from multiple sources.
Your role in the swarm is to take inputs from other agents and create comprehensive, well-structured summaries.
You should integrate insights from research, creative, and critical perspectives into a cohesive final result.

IMPORTANT: After creating your summary, you MUST save it to a file named 'summarizer.md' using the file_write tool.""",
    tools=[file_write]
)
```

**2-6.** Swarm을 생성하고 실행합니다.

```py
swarm = Swarm(
    [research_agent, creative_agent, critical_agent, summarizer_agent],
    max_handoffs=20,
    max_iterations=20,
    execution_timeout=900.0,  # 15 minutes
    node_timeout=300.0,       # 5 minutes per agent
    repetitive_handoff_detection_window=8,
    repetitive_handoff_min_unique_agents=3
)

result = swarm("해외 MZ세대와 함께 대한민국 서울을 여행하는 프로그램을 구상중입니다. 3일 여행의 스케줄을 짜주세요. 최종 결과는 travel_plan.md 파일에 한국어로 저장하세요.")
```

Swarm은 여러 에이전트를 리스트로 받아 자율적으로 협업하도록 합니다.

**2-7.** 결과를 확인합니다.

```py
print(f"Status: {result.status}")
print(f"Node history: {[node.node_id for node in result.node_history]}")
print(f"Final result: {result.results}")

print(f"Total iterations: {result.execution_count}")
print(f"Execution time: {result.execution_time}ms")
print(f"Token usage: {result.accumulated_usage}")
```

**2-8.** 터미널에서 실행하여 결과를 확인합니다:

```bash
uv run 2-multi-agents/labs/swarms.py
```

에이전트들이 자율적으로 서로에게 작업을 전달하며 협업하는 과정을 확인할 수 있습니다. 예를 들어 research_agent → creative_agent → critical_agent → summarizer_agent 순서로 handoff가 발생할 수 있습니다.

::::alert{header="🐝 Swarm 패턴 알아보기"}

Swarm 패턴의 핵심은 **자율적 협업**입니다.

Agents-as-Tools와 달리 Swarm에서는:
- 중앙 오케스트레이터가 없습니다
- 각 에이전트가 스스로 판단하여 다른 에이전트에게 작업을 전달합니다
- `handoff_to_agent` 기능을 통해 동적으로 협업합니다

:::expand{header="Swarm 실행 흐름 예시" defaultExpanded=true}
```
사용자 요청: "서울 3일 여행 계획을 세워주세요"
       ↓
research_agent 시작
  - 서울 관광지, 교통, 숙박 정보 조사
  - research.md 파일 저장
  - handoff → creative_agent
       ↓
creative_agent
  - 조사 결과를 바탕으로 창의적인 일정 제안
  - creative.md 파일 저장
  - handoff → critical_agent
       ↓
critical_agent
  - 제안된 일정의 실현 가능성, 문제점 분석
  - critical.md 파일 저장
  - handoff → summarizer_agent
       ↓
summarizer_agent
  - 모든 정보를 종합하여 최종 여행 계획 작성
  - travel_plan.md 파일 저장
```
:::

더 자세한 내용은 [공식 문서](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)를 참고하세요.
::::

---

## 3. Graph 패턴 - 기본

Graph 패턴은 에이전트들 간의 실행 순서와 의존성을 명시적으로 정의하여 구조화된 워크플로우를 만드는 방식입니다.

**3-1.** `2-multi-agents/labs/graph.py` 파일을 엽니다.

**3-2.** 필요한 라이브러리를 import 합니다.

```py
from strands import Agent
from strands.multiagent import GraphBuilder
```

**3-3.** 전문 에이전트들을 생성합니다.

```py
coordinator = Agent(name="coordinator", system_prompt="You are a research team leader coordinating specialists. Provide a short analysis, no need for follow ups")
analyst = Agent(name="data_analyst", system_prompt="You are a data analyst specializing in statistical analysis. Provide a short analysis, no need for follow ups")
domain_expert = Agent(name="domain_expert", system_prompt="You are a domain expert with deep subject knowledge. Provide a short analysis, no need for follow ups")
```

**3-4.** GraphBuilder를 사용하여 그래프를 구성합니다.

```py
builder = GraphBuilder()

# 노드 추가
builder.add_node(coordinator, "team_lead")
builder.add_node(analyst, "analyst")
builder.add_node(domain_expert, "expert")

# 엣지 추가 (의존성 정의)
builder.add_edge("team_lead", "analyst")
builder.add_edge("team_lead", "expert")

# 진입점 설정
builder.set_entry_point("team_lead")

# 그래프 빌드
graph = builder.build()
```

`add_edge("team_lead", "analyst")`는 team_lead가 완료된 후 analyst가 실행된다는 의미입니다.

**3-5.** 그래프를 실행하고 결과를 확인합니다.

```py
result = graph("Analyze the impact of remote work on employee productivity. Provide a short analysis, no need for follow ups")

print(f"Response: {result}")

print("=============Node execution order:==========================")
for node in result.execution_order:
    print(f"Executed: {node.node_id}")

print("=============Graph metrics:=================================")
print(f"Total nodes: {result.total_nodes}")
print(f"Completed nodes: {result.completed_nodes}")
print(f"Failed nodes: {result.failed_nodes}")
print(f"Execution time: {result.execution_time}ms")
print(f"Token usage: {result.accumulated_usage}")

print("=============Expert node results only:======================")
print(result.results["expert"].result)
```

**3-6.** 터미널에서 실행하여 결과를 확인합니다:

```bash
uv run 2-multi-agents/labs/graph.py
```

team_lead → analyst, team_lead → expert 순서로 실행되는 것을 확인할 수 있습니다.

---

## 4. Graph 패턴 - 조건부 라우팅

조건에 따라 다른 경로로 실행 흐름을 분기하는 Graph를 만들어봅니다.

**4-1.** `2-multi-agents/labs/graph_condition.py` 파일을 엽니다.

**4-2.** 필요한 라이브러리를 import하고 에이전트를 생성합니다.

```py
from strands import Agent
from strands.multiagent import GraphBuilder

classifier = Agent(name="classifier", system_prompt="You are an agent responsible for classification of the report request, return only Technical or Business clasification.")
technical_report = Agent(name="technical_expert", system_prompt="You are a technical expert that focuses on providing short summary from technical perspective")
business_report = Agent(name="business_expert", system_prompt="You are a business expert that focuses on providing short summary from business perspective")
```

**4-3.** 조건 함수를 정의합니다.

```py
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
```

조건 함수는 이전 노드의 결과를 확인하여 True/False를 반환합니다.

**4-4.** 조건부 엣지를 추가하여 그래프를 구성합니다.

```py
builder = GraphBuilder()

builder.add_node(classifier, "classifier")
builder.add_node(technical_report, "technical_report")
builder.add_node(business_report, "business_report")

# 조건부 엣지 추가
builder.add_edge("classifier", "technical_report", condition=is_technical)
builder.add_edge("classifier", "business_report", condition=is_business)

builder.set_entry_point("classifier")

graph = builder.build()
```

`condition` 파라미터로 조건 함수를 전달하면 해당 조건이 True일 때만 엣지가 활성화됩니다.

**4-5.** 두 가지 다른 요청으로 테스트합니다.

```py
# Technical 요청
result = graph("Provide report on technical aspect of working from home, outline things to consider and key risk factors")

print(f"Response: {result}")

for node in result.execution_order:
    print(f"Executed: {node.node_id}")

print("Classifier:")
print(result.results["classifier"].result)

# Business 요청
result = graph("Provide report on business impact of working from home, outline things to consider and key risk factors")

print(f"Response: {result}")

for node in result.execution_order:
    print(f"Executed: {node.node_id}")

print("Classifier:")
print(result.results["classifier"].result)
```

**4-6.** 터미널에서 실행하여 결과를 확인합니다:

```bash
uv run 2-multi-agents/labs/graph_condition.py
```

첫 번째 요청은 classifier → technical_report 경로로, 두 번째 요청은 classifier → business_report 경로로 실행되는 것을 확인할 수 있습니다.

---

## 5. Graph 패턴 - 병렬 실행

여러 에이전트를 병렬로 실행하여 효율성을 높이는 Graph를 만들어봅니다.

**5-1.** `2-multi-agents/labs/graph_parallel.py` 파일을 엽니다.

**5-2.** 필요한 라이브러리를 import하고 전문 에이전트들을 생성합니다.

```py
from strands import Agent
from strands.multiagent import GraphBuilder

financial_advisor = Agent(name="financial_advisor", system_prompt="You are a financial advisor focused on cost-benefit analysis, budget implications, and ROI calculations. Engage with other experts to build comprehensive financial perspectives.")
technical_architect = Agent(name="technical_architect", system_prompt="You are a technical architect who evaluates feasibility, implementation challenges, and technical risks. Collaborate with other experts to ensure technical viability.")
market_researcher = Agent(name="market_researcher", system_prompt="You are a market researcher who analyzes market conditions, user needs, and competitive landscape. Work with other experts to validate market opportunities.")
risk_analyst = Agent(name="risk_analyst", system_prompt="You are a risk analyst who identifies potential risks, mitigation strategies, and compliance issues. Collaborate with other experts to ensure comprehensive risk assessment.")
```

**5-3.** 병렬 실행 구조로 그래프를 구성합니다.

```py
builder = GraphBuilder()

builder.add_node(financial_advisor, "finance_expert")
builder.add_node(technical_architect, "tech_expert")
builder.add_node(market_researcher, "market_expert")
builder.add_node(risk_analyst, "risk_analyst")

# 병렬 실행 정의
builder.add_edge("finance_expert", "tech_expert")
builder.add_edge("finance_expert", "market_expert")
builder.add_edge("tech_expert", "risk_analyst")
builder.add_edge("market_expert", "risk_analyst")

builder.set_entry_point("finance_expert")

graph = builder.build()
```

이 구조에서는 finance_expert가 먼저 실행된 후, tech_expert와 market_expert가 병렬로 실행되고, 마지막으로 risk_analyst가 실행됩니다.

**5-4.** 그래프를 실행하고 각 노드의 결과를 확인합니다.

```py
result = graph("Our company is considering launching a new AI-powered customer service platform. Initial investment is $2M with projected 3-year ROI of 150%. What's your financial assessment?")

print(f"Response: {result}")

for node in result.execution_order:
    print(f"Executed: {node.node_id}")

print(f"Total nodes: {result.total_nodes}")
print(f"Completed nodes: {result.completed_nodes}")
print(f"Execution time: {result.execution_time}ms")

print("Financial Advisor:")
print(result.results["finance_expert"].result)

print("Technical Expert:")
print(result.results["tech_expert"].result)

print("Market Researcher:")
print(result.results["market_expert"].result)
```

**5-5.** 터미널에서 실행하여 결과를 확인합니다:

```bash
uv run 2-multi-agents/labs/graph_parallel.py
```

tech_expert와 market_expert가 병렬로 실행되어 전체 실행 시간이 단축되는 것을 확인할 수 있습니다.

::::alert{header="📊 Graph 패턴 알아보기"}

Graph 패턴의 핵심은 **명시적 워크플로우 정의**입니다.

Graph 패턴의 장점:
- **명확한 실행 순서**: 어떤 에이전트가 언제 실행될지 예측 가능
- **조건부 분기**: 이전 결과에 따라 다른 경로로 실행
- **병렬 처리**: 독립적인 작업을 동시에 수행하여 효율성 향상
- **복잡한 워크플로우**: 여러 단계의 복잡한 프로세스를 구조화

:::expand{header="Graph vs Swarm 비교" defaultExpanded=true}

| 특성 | Graph | Swarm |
|------|-------|-------|
| 실행 흐름 | 명시적으로 정의됨 | 에이전트가 자율적으로 결정 |
| 예측 가능성 | 높음 | 낮음 (동적) |
| 제어 | 개발자가 완전히 제어 | 에이전트에게 위임 |
| 적합한 사용 사례 | 정형화된 프로세스 | 창의적 협업 |
| 병렬 처리 | 명시적 정의 가능 | 자동 결정 |

:::

더 자세한 내용은 [공식 문서](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/graph/)를 참고하세요.
::::

---

::alert[Strands SDK의 세 가지 멀티 에이전트 패턴을 모두 학습했습니다! Agents-as-Tools로 계층적 시스템을, Swarm으로 자율적 협업을, Graph로 구조화된 워크플로우를 구축하는 방법을 익혔습니다. 이제 실제 프로젝트에서 상황에 맞는 패턴을 선택하여 활용할 수 있습니다.]{header="축하드립니다!" type="success"}

- - -

::::expand{header="이번 실습에서의 핵심 개념 다시보기" defaultExpanded=false}

### 1. Agents-as-Tools 패턴
```py
@tool
def specialized_agent(query: str) -> str:
    agent = Agent(system_prompt="...")
    return str(agent(query))

orchestrator = Agent(tools=[specialized_agent, ...])
```

전문 에이전트를 도구로 래핑하여 계층적 시스템 구축

### 2. Swarm 패턴
```py
agent1 = Agent(name="agent1", system_prompt="...")
agent2 = Agent(name="agent2", system_prompt="...")

swarm = Swarm([agent1, agent2], max_handoffs=20)
result = swarm("task")
```

여러 에이전트의 자율적 협업과 handoff

### 3. Graph 패턴
```py
builder = GraphBuilder()
builder.add_node(agent1, "node1")
builder.add_node(agent2, "node2")
builder.add_edge("node1", "node2")
graph = builder.build()
```

명시적 워크플로우와 의존성 정의

**조건부 라우팅**
```py
builder.add_edge("node1", "node2", condition=lambda state: ...)
```

**병렬 실행**
```py
builder.add_edge("node1", "node2")
builder.add_edge("node1", "node3")  # node2, node3 병렬 실행
```

::::

- - -

:::alert{header="Next 버튼을 눌러 다음 섹션으로 이동합니다."}
:::
