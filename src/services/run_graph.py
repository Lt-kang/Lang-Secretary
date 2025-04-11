from src.chains.graph_builder import build_graph


GRAPH = build_graph()

def run_main_flow(input_text: str) -> str:
    inputs = {"input": input_text}
    outputs = GRAPH.invoke(inputs)
    return outputs["output"]
