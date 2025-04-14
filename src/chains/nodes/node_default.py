from src.chains.llm_regeistry import default_llm


'''
추후 default prompt 작성
'''
def fallback_node(state):
    user_input = state["input"]
    result = default_llm.invoke(user_input)
    return {"response": result.content}



# if __name__ == "__main__":
#     while True:
#         input_text = input("<<text>> input: ")
#         if input_text == "exit":
#             break
    
#         print(fallback_node({"input": input_text}))
