from langchain_core.runnables import Runnable




def categorize_node(state:dict, chain: Runnable) -> Runnable:
    '''
    state: graph state
    chain: langchain runnable chain

    only categorize input and return route
    '''
    user_input = state["input"]
    result = chain.invoke(user_input)
    return {"input": user_input, "route": result.strip()}



def generate_node(state: dict, chain: Runnable) -> Runnable:
    '''
    state: graph state
    chain: langchain runnable chain
    '''
    user_input = state["input"]
    result = chain.invoke(user_input)

    if isinstance(result, str):
        return {"response": result.strip()}
    else:
        return {"response": result['output']}
