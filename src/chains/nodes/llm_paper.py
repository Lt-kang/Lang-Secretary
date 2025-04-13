from src.chains.llm_regeistry import paper_rag_chain


'''
추후 default prompt 작성
'''
def paper_node(state):
    user_input = state["input"]
    result = paper_rag_chain.run(user_input)
    return {"response": result.content}



# if __name__ == "__main__":
#     while True:
#         input_text = input("<<text>> input: ")
#         if input_text == "exit":
#             break
    
#         print(fallback_node({"input": input_text}))
