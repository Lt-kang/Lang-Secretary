from mcp import ClientSession, StdioServerParameters 
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent


from src.config import WEATHER_MCP_PORT, normal_storage_config
import os    

from src.core.chain_registry import (
    supervisor_chain, 
    default_chain, 
    paper_chain, 
    weather_chain,

    paper_llm,
    weather_llm,
)




def supervisor_node(state:dict):
    user_input = state["user_input"]
    result = supervisor_chain.invoke(user_input)
    state["route"] = result.strip()
    return state


def memory_input_node(state:dict, memory):
    memory.human_message_save(state["user_input"])
    state["user_input"] = memory.get_chat_history(state["user_input"])
    return state

def memory_save_node(state:dict, memory):
    memory.ai_message_save(state["final_answer"])
    return state

def default_answer_node(state:dict):
    result = default_chain.invoke(state["user_input"])
    state["final_answer"] = result
    return state



# async def call_weather_mcp(state:dict):
#     server_params = StdioServerParameters(
#         command="python", 
#         args=[os.getcwd() + r"\src\mcp_server\weather\weather_mcp_stdio.py"]
#     )

#     # print(os.getcwd() + r"\src\mcp_server\weather\weather_mcp_stdio.py")

#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             await session.initialize()

#             tools = await load_mcp_tools(session)

#             agent = create_react_agent(weather_llm, tools)


#             user_input = state['user_input']
#             inputs = {"messages": [("human", user_input)]}

#             result = await agent.ainvoke(inputs)
#     state['final_answer'] = result['messages'][-1].content
#     return state


async def call_weather_mcp(state:dict):
    weather_server_info = {
            "weather": {
                "url": f"http://localhost:{WEATHER_MCP_PORT}/sse",
                "transport": "sse",
            }
        }
    client = MultiServerMCPClient(weather_server_info)
    weather_tools = await client.get_tools()
    agent = create_react_agent(weather_llm, weather_tools)

    user_input = state['user_input']
    inputs = {"messages": [("human", user_input)]}

    result = await agent.ainvoke(inputs)
    state['final_answer'] = result['messages'][-1].content
    return state



from src.core.db.search import search_arxiv_id
from src.core.db.commit import save_document, save_paper_info
from langchain.prompts import PromptTemplate

from src.agents.arxiv_tools import (
    extract_arxiv_id,
    load_arxiv_document,
    extract_metadata_from_arxiv_result
)

arxiv_agent = create_react_agent(paper_llm, tools=[extract_arxiv_id])
def check_duplicated_arxiv_id(state:dict):
    try:

        
        inputs = {"messages": [("system", """
                                            extract_arxiv_id을 사용하여 
                                            사용자의 입력을 받아 올바른 형식의 arxiv_id 혹은 arxiv_url을 추출하세요.
                                            별도의 메시지를 출력하지 말고 오직 추출된 arxiv_id 혹은 arxiv_url을 반환하세요.
                                            만약 arxiv.org 도메인의 url을 입력 받았다면 arxiv_id를 추출해주세요.
                                            arxiv_id는 해당 url의 마지막 부분을 의미합니다.
                                
                                        ex) https://arxiv.org/pdf/2210.03629 다운 받아 -> 2210.03629
                                        """),
                            ("human", f'{state["user_input"].split("Human:")[-1].strip()} ~ 이 문장에서 arxiv_id를 추출해주세요.')]}
        
        print(f'{state["user_input"].split("Human:")[-1].strip()} 이 문장에서 arxiv_id를 추출해주세요.')
        arxiv_id = arxiv_agent.invoke(inputs)['messages'][-1].content
        print(arxiv_id)

        if arxiv_id:
            duplicated_result = search_arxiv_id(arxiv_id)
            state["paper_arxiv_id"] = arxiv_id
            state["paper_duplicated_check"] = "true" if duplicated_result else "false"
            state["final_answer"] = "이미 저장된 논문입니다." if duplicated_result else "저장되지 않은 논문입니다."
            return state
        
        state["final_answer"] = "arxiv_id를 찾을 수 없습니다."
        return state
    
    except Exception as e:
        state["final_answer"] = f"오류가 발생했습니다. 다시 시도해주세요. {e}"
        state["paper_duplicated_check"] = "error"
        return state



from pathlib import Path
normal_storage_path = normal_storage_config['save_path']
def save_paper(state:dict):
    # arxiv paper 객체 로드
    paper_arxiv_obj = load_arxiv_document(state["paper_arxiv_id"]) # 최신 arxiv_id를 얻기 위해 다시 load 함.

    arxiv_id = paper_arxiv_obj.entry_id.split('/')[-1]
    state['paper_arxiv_id'] = arxiv_id


    # arxiv paper 객체를 통해 논문 다운로드
    save_path = Path(normal_storage_path) / arxiv_id
    os.makedirs(save_path, exist_ok=True)
    paper_arxiv_obj.download_pdf(dirpath=save_path, filename=f"{arxiv_id}.pdf")


    # vector db에 저장
    save_document(paper_arxiv_obj)

    # sqlite3에 저장
    metadata = extract_metadata_from_arxiv_result(paper_arxiv_obj)
    inputs = {"messages": [("system", """
                                        입력 받은 text를 한국어로 번역해줍니다.
                                        별도의 답변은 필요 없이 번역된 문장만 반환해주세요.
                                        단, 이는 논문의 abstract에 대한 내용이기 때문에 고유명사, 혹은 전문기술을 뜻하는 용어면
                                        한국어로 번역하지 말고 원문 그대로 남겨주세요.
                                      """),
                           ("human", metadata["abstract"])]}
    abstract = arxiv_agent.invoke(inputs)['messages'][-1].content
    state["paper_summary"] = abstract

    paper_info = {"arxiv_id": arxiv_id,
                  "arxiv_url": metadata["pdf_url"],
                  "title": metadata["title"],
                  "abstract": abstract,
                  "created_at": None}
    save_paper_info(paper_info)
    return state


def summary_paper(state:dict):
    inputs = {"messages": [("system", """
    human input은 논문의 abstract를 번역한 내용 입니다.
    이를 바탕으로 논문의 내용을 요약해주세요.
                            
    단, 사용자에게 답변할 때에는 아래와 같은 양식을 따라주세요.
    
                            
    # [논문 title / 원문 그대로 작성해주세요.]
                            
    # Abstract
    [논문의 abstract / 이때 .뒤에 개행을 반드시 넣어주세요. 이는 사용자가 읽을 때 가독성을 향상 시키기 위함 입니다.]
                            
    # Summary
    [논문의 요약]
                            
    # Keyword
    [논문의 키워드 / 논문의 키워드는 기술명 중심으로 정리해줘. 이 논문을 이해하기 위해서 이 키워드는 알아야한다. 이런 부분들에 대해 작성해줘]
                            
    # reference
    [해당 논문을 더 깊게 이해하기 위한 추천 논문 목록]
                            
    또한 사용자가 보기 편하도록 당신이 어느정도의 구조화를 해주는 것이 좋습니다.
    또한 markdown 파일로 저장할 것이기 때문에 당신이 적절한 마크다운 형식으로 답변해주세요.
                                        """),
                           ("human", state["paper_summary"])]}
    answer = arxiv_agent.invoke(inputs)['messages'][-1].content
    state["final_answer"] = answer

    with open(Path(normal_storage_path) / state["paper_arxiv_id"] / f"{state['paper_arxiv_id']}.md", "w", encoding="utf-8") as f:
        f.write(answer)
    return state



