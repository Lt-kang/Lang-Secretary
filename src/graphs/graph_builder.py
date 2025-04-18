from langgraph.graph import StateGraph



from src.chains.chain_registry import categorize_chain, weather_chain, paper_chain, study_chain, default_chain
from src.core.node import generate_node, categorize_node
from src.schema.graph import GraphState




router_mapping = {
    "날씨": "weather",
    "논문": "paper",
    "기타": "default"
}
def route_logic(state):
    route = state["route"].lower()
    return router_mapping.get(route, "default")




def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("categorize", lambda state: categorize_node(state, categorize_chain))
    graph.add_node("weather", lambda state: generate_node(state, weather_chain))
    graph.add_node("paper", lambda state: generate_node(state, paper_chain))
    graph.add_node("study", lambda state: generate_node(state, study_chain))
    graph.add_node("default", lambda state: generate_node(state, default_chain))


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