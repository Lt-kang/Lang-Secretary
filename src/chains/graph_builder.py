from langgraph.graph import StateGraph
from typing import TypedDict


from src.chains.nodes import llm_categorize, llm_default, llm_paper, llm_weather, llm_study


class GraphState(TypedDict):
    input: str
    route: str
    response: str




router_mapping = {
    "날씨": "weather",
    "논문": "paper",
    "키워드": "study"
}
def route_logic(state):
    route = state["route"].lower()
    return router_mapping.get(route, "default")


'''
test code
'''
# def route_logic(state):
#     route = state["route"].lower()
#     if "감성" in route:
#         print("감성")
#         return "emotional"
#     elif "기술" in route:
#         print("기술")
#         return "technical"
#     elif "정보" in route or "검색" in route:
#         print("검색")
#         return "rag"
#     else:
#         print("default")
#         return "default"
    


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("categorize", llm_categorize.categorize_input)
    graph.add_node("weather", llm_weather.weather_node)
    graph.add_node("paper", llm_paper.paper_node)
    graph.add_node("study", llm_study.study_node)
    graph.add_node("default", llm_default.fallback_node)

    graph.set_entry_point("categorize")

    graph.add_conditional_edges("categorize", route_logic)

    graph.set_finish_point("weather")
    graph.set_finish_point("paper")
    graph.set_finish_point("study")
    graph.set_finish_point("default")

    runnable_chain = graph.compile()
    return runnable_chain
    


if __name__ == "__main__":
    print("<<<<<<<<<<<<<<<<<<< test conversation >>>>>>>>>>>>>>>>>>>")
    runnable_chain = build_graph()
    while True:
        user_input = input(f"\nUser: ")
        if user_input.lower() == "exit":
            print("Program exit")
            break

        result = runnable_chain.invoke({"input": user_input})
        print(f"LangGraph-bot: {result['response']}")