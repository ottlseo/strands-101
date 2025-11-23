from strands import Agent
from tools import python_repl_tool, bash_tool

agent = Agent(
    tools=[bash_tool, python_repl_tool]
    )

if __name__ == "__main__":
    user_input = "Hello world를 출력하는 파이썬 코드를 작성하고 실행시켜줄래?"
    # user_input = "completed 폴더에 무슨 파일 있는지 확인해줘"

    response = agent(user_input) 
