from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType
import requests
from pydantic import BaseModel

from src.chains.llm_regeistry import paper_llm
from src.config import VERBOSE



'''
TODO
vector db에 이미 저장된 논문인지 중복 여부를 확인하는 함수
'''
def find_duplicated_paper_in_vector_db(paper_title:str, paper_url:str) -> str:
    ...
    # vector DB 내 meta data를 조회하여 중복 여부를 확인

'''
TODO
url에서 논문을 다운받는 함수
'''
def download_paper_from_url(paper_url:str) -> str:
    ...
    # 논문을 다운받아 저장 
    
'''
TODO
벡터 데이터베이스에 논문을 저장하는 함수
'''
def save_paper_to_vector_db(paper_title:str, paper_url:str) -> str:
    ...
    # 저장 후 Vector DB에 저장

'''
TODO
논문을 한국어로 번역하는 함수
'''
def translate_paper_to_korean(paper_title:str, paper_url:str) -> str:
    ...

'''
TODO
논문을 요약하는 함수
'''
def summarize_paper(paper_title:str, paper_url:str) -> str:
    ...

'''
TODO
논문 데이터를 markdown 형식으로 추출하는 함수
'''
def extract_paper_data_to_markdown(paper_title:str, paper_url:str) -> str:
    ...


class PaperInput(BaseModel):
    paper_title: str
    paper_url: str


tools = [Tool(
    name="find_duplicated_paper_in_vector_db",
    description="...",
    func=find_duplicated_paper_in_vector_db,
    args_schema=PaperInput
    )
]


paper_agent_executor = initialize_agent(
    tools=tools,
    llm=paper_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=VERBOSE
)

if __name__ == "__main__":
    response = paper_agent_executor.invoke({"input": "https://arxiv.org/pdf/2210.03629 이 링크 들어가서 논문 다운받고 db에 저장해"})
    print(response)
    
