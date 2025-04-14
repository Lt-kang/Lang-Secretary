# from src.chains.llm_regeistry import weather_llm


# '''
# 추후 default prompt 작성
# '''
# def weather_node(state):
#     user_input = state["input"]
#     result = weather_llm.invoke(user_input)
#     return {"response": result.content}

from src.agents.weather_agent import weather_agent_executor

def weather_node(state):
    user_input = state["input"]
    result = weather_agent_executor.invoke({"input": user_input})
    return {"response": result.content}



