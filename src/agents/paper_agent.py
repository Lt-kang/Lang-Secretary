from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from pydantic import BaseModel

from src.chains.llm_regeistry import paper_llm, vector_db
from src.config import VERBOSE
from src.utils.arxiv_tools import load_arxiv_document


'''
TODO
vector db에 이미 저장된 논문인지 중복 여부를 확인하는 함수
'''
def find_duplicated_paper_in_vector_db(paper_title:str, paper_url:str) -> str:
    ...
    # vector DB 내 meta data를 조회하여 중복 여부를 확인

    
'''
arxiv 라이브러리를 통해 논문을 다운받아 Document 형식으로 반환
'''
def load_paper_to_arxiv(page_info:str) -> str | Document:
    '''
    page_info: 논문 제목 혹은 논문 링크

    논문 제목 or 링크를 입력 받아서 필요한 부분을 parsing하고 
    parsing한 arxiv_id를 통해 arxiv 라이브러리로 해당 논문을 Document 형식으로 반환
    이후 vector db에 저장
    '''

    content, metadata = load_arxiv_document(page_info)
    if content is None:
        return "논문 Load 실패"
    else:
        return Document(page_content=content, metadata=metadata)


'''
TODO
load_paper_to_arxiv 함수를 통해 반환된 Document 형식의 데이터를 vector db에 저장
'''
def save_paper_to_vector_db(document:Document) -> str:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents([document])

    vector_db.add_documents(split_docs)
    vector_db.persist()

    return (document, "논문 저장 완료")

    

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
    
