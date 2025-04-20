from langchain_community.document_loaders import ArxivLoader

import arxiv
import re

from src.core.config import PAPER_SAVE_DIR



'''
사용자 입력: "{url | title | id} 이거 저장해"


if url | id
1. extract_arxiv_id(input_str) 호출 -> arxiv_id 추출
2. load_arxiv_document(arxiv_id) 호출 -> metadata 추출 -> arxivLoader 호출 후 Document 반환 -> vector_db에 저장
3. arxiv_paper_download(paper) 호출 -> 논문 다운로드

if title
1. load_arxiv_document(title) 호출 -> metadata 추출 -> arxivLoader 호출 후 Document 반환 -> vector_db에 저장
2. arxiv_paper_download(paper) 호출 -> 논문 다운로드
'''


'''
TODO
paper title로 입력 받은 경우 추가
'''
def extract_arxiv_id(user_input:str) -> str:
    '''
    user_input: 사용자의 입력
    '''

    # ex) "https://arxiv.org/pdf/2210.03629" / "https://arxiv.org/abs/2210.03629"
    user_input = user_input.replace("abs", "pdf")
    match = re.search(r'arxiv\.org/pdf/(\d{4}\.\d{5})(v\d+)?', user_input)
    if match:
        return f"{match.group(1)}"
    
    # "2210.03629v1"
    if isinstance(user_input, str):
        if re.match(r'\d{4}\.\d{5}(v\d+)?', str(user_input)):
            return f"{user_input}"
    
   
    return "해당 paper의 arxiv id를 찾을 수 없습니다."




def load_arxiv_document(arxiv_id: str) -> arxiv.Result:
    '''
    arxiv_id: arxiv id

    arxiv 라이브러리를 통해 논문을 다운받아 arxiv.Result 객체 반환
    '''

    try:
        search_by_id = arxiv.Search(id_list=[arxiv_id])
        paper = next(arxiv.Client().results(search_by_id))

        return paper
    
    except Exception as e:
        return None



def arxiv_paper_download(paper: arxiv.Result) -> str:
    '''
    arxiv.Result 객체를 통해 논문을 다운 받아서 저장함.
    '''
    try:
        paper.download_pdf(dirpath=PAPER_SAVE_DIR, filename=f"{paper.entry_id.split('/')[-1]}.pdf")
        return f"논문을 다운받았습니다. 파일 위치: {PAPER_SAVE_DIR}/{paper.entry_id.split('/')[-1]}.pdf"

    except Exception as e:
        return f"논문을 다운받을 수 없습니다. {e}"



def arxiv_paper_to_doc_obj(paper: arxiv.Result):
    '''
    paper: arxiv.Result 객체

    arxiv.Result 객체를 Document 형식으로 반환
    '''
    if paper is None:
        return "논문을 Document 객체로 변환하는 과정에서 오류가 발생했습니다."
    
    loder = ArxivLoader(
        query=paper.title,
        load_max_docs=1,
    )
    docs = loder.load()
    target_doc = docs[0]

    target_doc.metadata = {
                            "title": paper.title,
                            "authors": ', '.join([author.name for author in paper.authors]),
                            "summary": paper.summary,
                            "pdf_url": paper.pdf_url,
                            "entry_id": paper.entry_id,
                            "arxiv_id": paper.entry_id.split("/")[-1],
                          }

    return target_doc


if __name__ == "__main__":
    user_input = "https://arxiv.org/pdf/2210.03629 다운 받아"

    arxiv_id = extract_arxiv_id(user_input)
    print(arxiv_id)


    paper = load_arxiv_document(arxiv_id)
    print(paper)

    result = arxiv_paper_download(paper)
    print(result)

    doc_obj = arxiv_paper_to_doc_obj(paper)
    print(doc_obj)

