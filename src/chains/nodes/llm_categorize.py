from src.chains.llm_regeistry import categorize_llm




'''
추후 1개의 input에 여러개의 요청이 있을 경우 대비한 prompt

    prompt = f"""
    다음 문장이 어떤 유형에 더 유사한지 골라주세요.


    답변은 반드시 단어로만 해줘 [날씨, 논문, 키워드]
    만약 여러개가 해당된다고 생각한다면 쉼표로 구분해서 출력해줘
    아래는 예시야
    예시1 날씨, 논문
    예시2 날씨, 키워드
    
    문장: "{user_input}"
    """
'''
def categorize_input(state):
    user_input = state["input"]
    prompt = f"""
    다음 문장이 어떤 유형에 더 유사한지 골라주세요.

    답변은 반드시 단어로만 해주세요. [날씨, 논문, 키워드]
    
    문장: "{user_input}"
    """
    result = categorize_llm.invoke(prompt)
    return {"input": user_input, "route": result.content.strip()}



if __name__ == "__main__":
    while True:
        input_text = input("<<text>> input: ")
        if input_text == "exit":
            break
    
        print(categorize_input({"input": input_text}))
