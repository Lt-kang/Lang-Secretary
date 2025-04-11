from langchain_openai import ChatOpenAI
from app.config import OPENAI_API_KEY


llm_classifier = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
llm_emotional = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=OPENAI_API_KEY)
llm_tech = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)
llm_rag = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)



if __name__ == "__main__":
    print(llm_classifier.invoke("Hello, world!"))
