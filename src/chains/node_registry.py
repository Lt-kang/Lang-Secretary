from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document

from langgraph.graph import StateGraph, END
from typing import TypedDict




llm_classifier = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
llm_emotional = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=OPENAI_API_KEY)
llm_tech = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)
llm_rag = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)


# -----------------------
# 2. VectorDB (FAISS) 예시 세팅
# -----------------------
# 간단한 문서 예시
docs = [Document(page_content="LangGraph is a framework for building LLM state machines."),
        Document(page_content="LangChain is a framework for composing LLM applications.")]

embedding = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embedding)
retriever = vectorstore.as_retriever()

rag_chain = RetrievalQA.from_chain_type(llm=llm_rag, retriever=retriever)

# -----------------------
# 3. 노드 정의
# -----------------------

# 분류 노드
def classify_input(state):
    user_input = state["input"]
    prompt = f"""
    다음 문장이 어떤 유형인지 골라주세요: [감성 대화 / 기술 질문 / 정보 검색]
    문장: "{user_input}"
    정답만 한 단어로 대답하세요.
    """
    result = llm_classifier.invoke(prompt)
    return {"input": user_input, "route": result.content.strip()}

# 감성 대화 노드
def emotional_node(state):
    user_input = state["input"]
    result = llm_emotional.invoke(f"공감해줘: {user_input}")
    return {"response": result.content}

# 기술 질문 노드
def tech_node(state):
    user_input = state["input"]
    result = llm_tech.invoke(f"기술적으로 설명해줘: {user_input}")
    return {"response": result.content}

# RAG 검색 노드
def rag_node(state):
    user_input = state["input"]
    result = rag_chain.run(user_input)
    return {"response": result}


# -----------------------
# 4. 라우터 정의
# -----------------------
# router_mapping = {
#     "감성": "emotional",
#     "기술": "technical",
#     "정보": "rag",
#     "검색": "rag"
# }
# def route_logic(state):
#     route = state["route"].lower()
#     return router_mapping.get(route, "emotional")

def route_logic(state):
    route = state["route"].lower()
    if "감성" in route:
        print("감성")
        return "emotional"
    elif "기술" in route:
        print("기술")
        return "technical"
    elif "정보" in route or "검색" in route:
        print("검색")
        return "rag"
    else:
        print("감성 by fallback")
        return "emotional"  # 기본적으로 감성 대화로 라우팅
        # return END  # 종료

 
# -----------------------
# 5. 그래프 구성
# -----------------------
class GraphState(TypedDict):
    input: str
    route: str
    response: str

graph = StateGraph(GraphState)

graph.add_node("classifier", classify_input)
graph.add_node("emotional", emotional_node)
graph.add_node("technical", tech_node)
graph.add_node("rag", rag_node)

graph.set_entry_point("classifier")

graph.add_conditional_edges("classifier", route_logic)

graph.set_finish_point("emotional")
graph.set_finish_point("technical")
graph.set_finish_point("rag")

runnable_chain = graph.compile()



if __name__ == "__main__":
    print(" test conversation ")
    while True:
        user_input = input(f"\nUser: ")
        if user_input.lower() == "exit":
            print("Program exit")
            break

        result = runnable_chain.invoke({"input": user_input})
        print(f"LangGraph-bot: {result['response']}")