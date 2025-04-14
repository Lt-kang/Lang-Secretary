from langgraph.graph import StateGraph
from typing import TypedDict


from src.chains.nodes import node_categorize, node_default, node_paper, node_study, node_weather


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
    

# paper node를 여러 단계로 구성할 예정
''' 예시 코드
graph = StateGraph(GraphState)

# 노드 등록
graph.add_node("classifier", classify_input)
graph.add_node("emotional", emotional_node)

# 기술 노드를 여러 단계로 구성
graph.add_node("tech_1", tech_node_1)
graph.add_node("tech_2", tech_node_2)

# 시작 노드
graph.set_entry_point("classifier")

# 분기 설정
graph.add_conditional_edges(
    "classifier",
    lambda state: state["route"],
    {
        "emotional": "emotional",
        "technical": "tech_1"  # 기술은 tech_1부터 시작
    }
)

# 기술 흐름 연결
graph.add_edge("tech_1", "tech_2")

# 종료 포인트 설정
graph.set_finish_point("emotional")
graph.set_finish_point("tech_2")

'''
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("categorize", node_categorize.categorize_input)
    graph.add_node("weather", node_weather.weather_node)
    graph.add_node("paper", node_paper.paper_node)
    graph.add_node("study", node_study.study_node)
    graph.add_node("default", node_default.fallback_node)

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