from langchain.agents import (
    initialize_agent, 
    AgentType
)

from src.agents.paper.agent import paper_tools
from src.agents.weather.agent import weather_tools

from src.chains.chain_registry import (
    paper_chain,
    weather_chain
)

from src.core.config import VERBOSE

'''
paper_agent
'''
paper_agent = initialize_agent(
    tools=paper_tools,
    llm=paper_chain,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=VERBOSE,
    handle_parse_errors=True,
    # max_iterations=5,
    # max_retries=3
)




# _paper_agent = create_structured_chat_agent(
#     llm=paper_chain,
#     tools=paper_tools,
#     prompt=PAPER_PROMPT
# )
# paper_agent = AgentExecutor(agent=_paper_agent, 
#                             verbose=VERBOSE,
#                             handle_parse_errors=True,
#                             max_iterations=5)



'''
weather_agent
'''
# weather_agent = initialize_agent (
#     tools=weather_tools,
#     llm=weather_chain,
#     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     handle_parse_errors=True,
#     # max_iterations=5,
#     # max_retries=3,
# )



weather_agent = initialize_agent(
    tools=weather_tools,
    llm=weather_chain,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parse_errors=True,
    # max_iterations=5,
    # max_retries=3,
)



if __name__ == "__main__":
    # print("================== paper_agent test ==================")
    # print(paper_agent.invoke("https://arxiv.org/abs/2210.03629 다운 받아서 vector db에 저장해"))
    # print(paper_agent.invoke("응 요약본도 알려줄래?"))
    # print("\n\n\n")
    # print("================== weather_agent test ==================")
    # print(weather_agent.invoke("오늘 날씨와 추천 복장 알려줘"))
    # print("\n\n\n")

    while True:
        user_input = input("input: ")
        print(paper_agent.invoke(user_input))
