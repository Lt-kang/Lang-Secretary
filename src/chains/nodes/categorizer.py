from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from src.config import OPENAI_API_KEY, ENV


if ENV == "dev":
    llm_classifier = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
else:
    llm_classifier = ChatOpenAI(model="gpt-4", temperature=0)



class CategoryData(BaseModel):
    category: str = Field(default=None, description="Category of the input")



'''

1. weather agent
2. paper_review agent
    2-a. arxiv download
    2-b. arxiv into vector db
    2-c. arxiv translate
    2-d. arxiv summary
    2-e. arxiv review
    2-f. arxiv md export
3. keyword save agent 
4. keyword recall and analyze agent
'''
def categorize_input(state):
    user_input = state["input"]
    prompt = f"""
    다음 문장이 어떤 유형에 더 유사한지 골라주세요.


    답변은 반드시 단어로만 해줘 [날씨, 논문, 키워드]
    만약 여러개가 해당된다고 생각한다면 쉼표로 구분해서 출력해줘
    아래는 예시야
    예시1 날씨, 논문
    예시2 날씨, 키워드
    
    문장: "{user_input}"
    """
    result = llm_classifier.invoke(prompt)
    return {"input": user_input, "route": result.content.strip()}



if __name__ == "__main__":
    while True:
        input_text = input("<<text>> input: ")
        if input_text == "exit":
            break
    
        print(categorize_input({"input": input_text}))
