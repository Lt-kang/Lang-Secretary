from langchain_openai import ChatOpenAI 
from langchain.chains import RetrievalQA

from src.core.vectordb import vector_db_connection


# Prompt Template 사용을 고려해볼것
''' 예시 코드
from langchain_core.prompts import PromptTemplate

emotional_template = PromptTemplate.from_template(
    "사용자의 말에 위로가 되는 감정적 대답을 해줘:\n사용자: {input}"
)
emotional_chain: Runnable = emotional_template | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
'''



'''
지식 관련된 내용은 정확한 답변 유도를 위해 temperature를 0으로 설정
'''
KNOWLEDGE_T  = 0

categorize_llm = ChatOpenAI(model="gpt-4.1-nano", temperature=KNOWLEDGE_T)
paper_llm = ChatOpenAI(model="gpt-4.1", temperature=KNOWLEDGE_T)
study_llm = ChatOpenAI(model="gpt-4.1", temperature=KNOWLEDGE_T)


'''
그 외 기타 답변에 대해서는 조금 더 유연한 답변을 위해 temperature를 0.3으로 설정
'''
DEFAULT_T = 0.3

weather_llm = ChatOpenAI(model="gpt-4.1", temperature=DEFAULT_T)
default_llm = ChatOpenAI(model="gpt-4.1", temperature=DEFAULT_T)



'''
RAG
paper LLM과 vector DB를 연결
'''
vector_db = vector_db_connection()
paper_retriever = vector_db.as_retriever()
paper_rag_chain = RetrievalQA.from_chain_type(llm=paper_llm, retriever=paper_retriever)



if __name__ == "__main__":
    print("<<<<<<<<<<<<<<<< llm api test >>>>>>>>>>>>>>>>>")
    print("<<<<<<<<<<<<<<<< categorize_llm >>>>>>>>>>>>>>>>>")
    print(categorize_llm.invoke("'정상'이라고만 대답해"))
    print("<<<<<<<<<<<<<<<< weather_llm >>>>>>>>>>>>>>>>>")
    print(weather_llm.invoke("'정상'이라고만 대답해"))
    print("<<<<<<<<<<<<<<<< paper_llm >>>>>>>>>>>>>>>>>")
    print(paper_llm.invoke("'정상'이라고만 대답해"))
    print("<<<<<<<<<<<<<<<< default_llm >>>>>>>>>>>>>>>>>")
    print(default_llm.invoke("'정상'이라고만 대답해"))
    print("<<<<<<<<<<<<<<<< study_llm >>>>>>>>>>>>>>>>>")
    print(study_llm.invoke("'정상'이라고만 대답해"))
