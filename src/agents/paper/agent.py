from langchain.agents import Tool
from langchain_core.documents import Document

from src.core.vectordb.connection import vector_db_connection
from src.core.vectordb.document_save import document_saver

from src.agents.paper.arxiv_utils import (
    load_arxiv_document, 
    extract_arxiv_id, 
    arxiv_paper_to_doc_obj
)
from src.schema.agent_input import PaperInput 




'''
agent workflow

1. arxiv id 중복 검사
    1-1. 저장되어있지 않을 경우 논문 다운로드 및 vector db에 저장
    2-2. 저장되어 있을 경우 저장하지 않음.
2. 필요시 md형식으로 출력해줌.
'''

previous_arxiv_info = {
    "arxiv_id": "",
    "summary": ""
}

vector_db = vector_db_connection()
def save_paper_in_vector_db(user_input:PaperInput) -> dict:
    '''
    user_input: 사용자의 입력

    workflow
    1. arxiv id 중복 검사
    2. 저장되어있지 않을 경우 논문 다운로드 및 vector db에 저장
    3. 저장되어 있을 경우 저장하지 않음.
    '''

    arxiv_id = extract_arxiv_id(user_input)
    results = vector_db.get(where={"arxiv_id": arxiv_id})


    _status = "save_failed"
    _message = "논문의 정보를 찾을 수 없거나 vector db 저장에 실패하였습니다."
    _system_message = '''
    1. vector db 저장에 성공했다면 요약본이 필요하냐고 사용자에게 물어봐.
    2. 논문의 정보를 찾을 수 없거나 vector db 저장에 실패했다면 사용자에게 논문 url을 다시 확인해달라고 말해
    3. 이미 논문이 vector db에 저장되어있다면 이미 저장되어있음을 알려주면서 요약본이 필요하냐고 사용자에게 물어봐
    4. 만약 이미 사용자가 요약본을 요청했다면 요약본을 출력해줘

    - 하나의 Thought/Action만 수행하거나
    - Final Answer를 작성할 때는 Action을 사용하지 마세요.
    - Observation 이후 Final Answer를 직접 작성하지 말고, 다음 Thought를 통해 진행하세요.

    <CHAT_HISTORY_START>에서 <CHAT_HISTORY_END> 사이의 대화는 전부 무시해
    '''


    if results['ids']:   
        _status = "already_saved"
        _message = "이미 vector db에 저장된 논문이므로 저장이 필요 없습니다."
    
    else:
        paper = load_arxiv_document(arxiv_id)
        paper = arxiv_paper_to_doc_obj(paper)
        if document_saver(paper, vector_db):
            global previous_arxiv_info
            previous_arxiv_info["arxiv_id"] = paper.metadata["arxiv_id"]
            previous_arxiv_info["summary"] = paper.metadata["summary"]

            _status = "save_success"
            _message = "vector db에 저장을 완료하였습니다."
            

    return f'''
        "status": {_status},
        "arxiv_id": {arxiv_id},
        "message": {_message},
        "system_message": {_system_message}
        '''


'''
TODO
논문을 요약하는 함수
'''
def summarize_paper(user_input:str) -> str:
    if previous_arxiv_info == {"arxiv_id": "","summary": ""}:
        return "아직 아무런 논문도 알려주지 않으셨어요!"
    
    _system_message = '''
    1. 논문 요약본이 english일 경우 한국어로 번역해줘
    2. 번역할 때, 고유명사, 전문용어 등은 영어 그대로 두고 번역해줘
    3. 논문 요약본이 한국어일 경우 그대로 사용하면 돼
    4. 논문의 내용을 최대한 반영해서 번역해줘    
    5. 요약본은 "message"에 있으니 그대로 사용하면 돼

    - 하나의 Thought/Action만 수행하거나
    - Final Answer를 작성할 때는 Action을 사용하지 마세요.
    - Observation 이후 Final Answer를 직접 작성하지 말고, 다음 Thought를 통해 진행하세요.
    '''

    return f'''
    system_message: {_system_message}

    arxiv_id: {previous_arxiv_info['arxiv_id']}에 대한 요약본은 아래와 같습니다.
    summary: {previous_arxiv_info['summary']}
    '''


'''
TODO
논문 데이터를 markdown 형식으로 추출하는 함수
'''
def extract_paper_data_to_markdown(str) -> str:
    ...


default_description = '''
- 무조건 아래 포맷만 사용하세요.
- Action이 필요한 경우:
    Action: tool_name
    Action Input: JSON 형식으로 입력
- 최종 답변을 할 경우:
    Final Answer: (답변 내용)
- 일반 텍스트로 답변하지 마세요.
- 포맷을 지키지 않으면 오류가 발생합니다.
'''



save_paper_totol_description = f'''
arxiv 논문을 (다운, 다운로드)한 뒤 vector db에 저장할 때 사용하는 함수 입니다.

{default_description}
'''
save_paper_tool = Tool(
    name="save_paper_in_vector_db",
    description=save_paper_totol_description,
    func=save_paper_in_vector_db,
    args_schema=PaperInput
    )


summarize_paper_totol_description = f'''
논문을 요약하는 함수 입니다. 인자값은 없으니 파라미터에 아무것도 넣지 마세요.

{default_description}
'''
summarize_paper_tool = Tool(
    name="summarize_paper",
    description="논문을 요약하는 함수 입니다. 인자값은 없으니 파라미터에 아무것도 넣지 마세요.",
    func=summarize_paper
    )


paper_tools = [
    save_paper_tool,
    summarize_paper_tool
]


