from langchain_openai import ChatOpenAI
from src.config import OPENAI_API_KEY


llm_classifier = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_emotional = ChatOpenAI(model="gpt-4", temperature=0.7)
llm_tech = ChatOpenAI(model="gpt-4", temperature=0)
llm_rag = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)



if __name__ == "__main__":
    print(llm_classifier.invoke("Hello, world!"))
