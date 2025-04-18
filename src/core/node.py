from langchain_core.runnables import Runnable




def generate_node(state: dict, chain: Runnable) -> Runnable:
    '''
    state: graph state
    chain: langchain runnable chain
    '''
    user_input = state["input"]
    result = chain.invoke(user_input)
    return {"response": result.content}
