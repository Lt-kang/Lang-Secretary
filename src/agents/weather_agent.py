from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
import requests


from src.chains.llm_regeistry import weather_llm



def weather_tool(expression: str) -> str:
    url = ...



tools = [Tool(
    name="weather_tool",
    description="지역을 입력 받아서 해당 지역의 날씨를 반환해주는 도구입니다.",
    func=weather_tool
),
]

# Step 3. Agent 초기화
weather_agent = initialize_agent(
    tools=tools,
    llm=weather_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

