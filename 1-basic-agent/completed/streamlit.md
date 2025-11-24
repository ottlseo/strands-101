# Strands Agent를 Streamlit으로 애플리케이션화하기

## 📌 개요

이 문서는 터미널에서 실행하던 Strands Agent (`basic.py`)를 Streamlit 웹 애플리케이션(`streamlit_app.py`)으로 변환하는 과정에서 고려한 사항과 전체적인 코드 흐름을 설명합니다.

---

## 🔄 basic.py vs streamlit_app.py 비교

### basic.py (터미널 실행)

```python
from strands import Agent
from strands_tools import calculator, current_time, use_aws, python_repl

agent = Agent(tools=[calculator, current_time, use_aws, python_repl])
response = agent("What is 80/4?")
print(response)
```

**특징:**
- 단일 실행 방식: 한 번의 질문과 답변으로 종료
- 동기 방식: `agent()` 호출 후 결과를 기다림
- 히스토리 없음: 이전 대화 기록이 유지되지 않음
- 단순 출력: `print()`로 결과만 출력

### streamlit_app.py (웹 애플리케이션)

**특징:**
- 지속적인 대화: 여러 번의 질문과 답변 가능
- 비동기 스트리밍: `stream_async()`로 실시간 응답 표시
- 히스토리 관리: 세션 상태로 대화 기록 유지
- 풍부한 UI: 도구 호출 과정, 결과를 시각적으로 표시

---

## 🎯 애플리케이션화 시 추가 고려사항

### 1. **세션 상태 관리 (Session State)**

Streamlit은 페이지가 새로고침될 때마다 코드가 재실행됩니다. 따라서 Agent 인스턴스와 대화 히스토리를 유지하기 위해 세션 상태를 사용합니다.

```python
# Agent 초기화 (세션 상태에 저장)
if "agent" not in st.session_state:
    st.session_state.agent = Agent(tools=[calculator, current_time, use_aws, python_repl])

# 채팅 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
```

**왜 필요한가?**
- Agent를 매번 재생성하면 설정과 상태가 초기화됨
- 대화 히스토리를 유지해야 이전 대화 내용을 볼 수 있음

### 2. **비동기 스트리밍 (Async Streaming)**

터미널에서는 결과를 한 번에 받아도 되지만, 웹 애플리케이션에서는 사용자 경험을 위해 실시간으로 응답을 보여주는 것이 좋습니다.

```python
# 비동기 스트림 실행
agent_stream = st.session_state.agent.stream_async(prompt)

async for event in agent_stream:
    if "data" in event:  # 텍스트 스트리밍
        text = event["data"]
        current_text += text
        current_text_box.info(current_text)
```

**왜 필요한가?**
- 사용자가 응답을 기다리는 동안 지루함을 느끼지 않음
- Agent가 어떤 작업을 하고 있는지 실시간으로 확인 가능
- 도구 호출 과정을 투명하게 보여줄 수 있음

### 3. **이벤트 기반 처리**

`stream_async()`는 여러 종류의 이벤트를 발생시킵니다. 각 이벤트를 적절히 처리해야 합니다.

| 이벤트 타입 | 설명 | 처리 방법 |
|------------|------|----------|
| `"data"` | Agent의 응답 텍스트 스트리밍 | 텍스트를 누적하여 파란색 박스에 표시 |
| `"current_tool_use"` | 도구 호출 시작 | 주황색 박스에 도구명과 입력 표시 |
| `"message"` | 도구 실행 결과 | 초록색 박스에 결과 표시 |
| `"result"` | 최종 응답 | 최종 텍스트 추출 |

### 4. **UI/UX 고려사항**

#### a) 채팅 히스토리 표시

```python
# 채팅 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            # 생각 과정 표시
            if message.get("thinking_steps"):
                with st.expander("🧠 생각 과정 보기", expanded=False):
                    for step in message["thinking_steps"]:
                        st.markdown(step)
            st.markdown(message["content"])
```

이전 대화를 스크롤하며 볼 수 있어야 합니다.

#### b) 실시간 피드백

도구를 호출할 때와 결과가 나올 때 사용자에게 시각적 피드백을 제공합니다.

- 🔧 주황색 박스: 도구 호출 중
- ✅ 초록색 박스: 도구 실행 완료
- 📘 파란색 박스: Agent 응답

#### c) 컨테이너 관리

Streamlit에서 동적으로 UI를 업데이트하려면 컨테이너를 적절히 관리해야 합니다.

```python
# 메인 컨테이너 생성
main_container = st.container()

# 텍스트 박스 동적 생성
if current_text_box is None:
    with main_container:
        current_text_box = st.empty()
        text_boxes.append(current_text_box)

# 업데이트
current_text_box.info(current_text)
```

### 5. **에러 핸들링**

웹 애플리케이션에서는 에러가 발생해도 앱이 죽지 않고 사용자에게 적절한 메시지를 보여줘야 합니다.

```python
try:
    # Agent 실행
    final_response, tool_info = asyncio.run(run_agent())
except Exception as e:
    import traceback
    error_message = f"오류가 발생했습니다: {str(e)}\n\n```\n{traceback.format_exc()}\n```"
    st.error(error_message)
    st.session_state.messages.append({"role": "assistant", "content": f"오류: {str(e)}"})
```

### 6. **대화 초기화 기능**

사용자가 새로운 대화를 시작하고 싶을 때를 위한 기능이 필요합니다.

```python
if st.button("대화 초기화"):
    st.session_state.messages = []
    st.rerun()
```

---

## 📊 전체 코드 흐름

### 1️⃣ 초기화 단계

```
페이지 설정 (제목, 아이콘)
    ↓
Agent 초기화 (세션 상태 확인)
    ↓
메시지 히스토리 초기화 (세션 상태 확인)
    ↓
이전 대화 히스토리 표시
```

### 2️⃣ 사용자 입력 처리

```
사용자가 메시지 입력
    ↓
메시지를 히스토리에 추가
    ↓
화면에 사용자 메시지 표시
```

### 3️⃣ Agent 실행 및 스트리밍

```
비동기 함수 run_agent() 정의
    ↓
stream_async() 시작
    ↓
이벤트 루프 시작
    │
    ├─ "data" 이벤트
    │   └─ 텍스트 누적 → 파란색 박스에 표시
    │
    ├─ "current_tool_use" 이벤트
    │   └─ 도구 정보 저장 → 주황색 박스에 표시
    │
    ├─ "message" 이벤트
    │   └─ 도구 결과 추출 → 초록색 박스에 표시
    │
    └─ "result" 이벤트
        └─ 최종 응답 추출
    ↓
비동기 함수 종료 (final_response, tool_info 반환)
```

### 4️⃣ 결과 표시 및 저장

```
최종 응답 표시
    ↓
도구 사용 정보로 reasoning_text 생성
    ↓
메시지를 히스토리에 저장
    ↓
페이지 리렌더링 (히스토리 업데이트)
```

---

## 🔑 핵심 차이점 요약

| 항목 | basic.py | streamlit_app.py |
|------|----------|------------------|
| **실행 방식** | 동기 (`agent()`) | 비동기 (`stream_async()`) |
| **실행 횟수** | 1회 실행 후 종료 | 지속적인 대화 가능 |
| **상태 관리** | 없음 | 세션 상태로 관리 |
| **히스토리** | 없음 | 대화 기록 유지 |
| **도구 가시성** | 터미널 로그만 | UI에 실시간 표시 |
| **사용자 경험** | 결과 대기 | 실시간 스트리밍 |
| **에러 처리** | 프로그램 종료 | 에러 메시지 표시 후 계속 |

---

## 💡 추가 개선 가능 사항

1. **대화 기록 저장**: 파일이나 데이터베이스에 대화 기록 저장
2. **다중 세션 지원**: 여러 대화 스레드 관리
3. **설정 UI**: 도구 선택, 모델 파라미터 조정 등
4. **파일 업로드**: 이미지, 문서 등을 Agent에 전달
5. **음성 입력/출력**: TTS/STT 통합
6. **사용자 인증**: 다중 사용자 지원

---

## 🎓 결론

Streamlit으로 Agent를 애플리케이션화하는 것은 단순히 UI를 추가하는 것 이상입니다. 세션 관리, 비동기 처리, 이벤트 핸들링, UX 개선 등 웹 애플리케이션 특유의 고려사항들이 필요합니다. 하지만 이를 통해 더 나은 사용자 경험을 제공하고, Agent의 작동 과정을 투명하게 보여줄 수 있습니다.
