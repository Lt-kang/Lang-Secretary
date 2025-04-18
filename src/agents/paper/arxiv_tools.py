from langchain_community.document_loaders import ArxivLoader
from langchain_core.documents import Document

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






def extract_arxiv_id(input_str: str) -> str:
    """
    [parameter]
    input_str = arXiv URL, ID, Title
    
    [instruction]
    arXiv URL, ID, 혹은 title 중에서 arXiv ID를 추출하거나 검색
    """

    '''[arXiv URL]
    ex)
    "https://arxiv.org/pdf/2210.03629"
    "https://arxiv.org/abs/2210.03629"
    '''
    match1 = re.search(r'arxiv\.org/pdf/(\d{4}\.\d{5})(v\d+)?', input_str)
    match2 = re.search(r'arxiv\.org/abs/(\d{4}\.\d{5})(v\d+)?', input_str)

    if match1:
        return match1.group(1)
    elif match2:
        return match2.group(1)



    '''[arXiv ID]
    ex)
    "2210.03629"
    "2210.03629v1"
    '''
    if re.match(r'\d{4}\.\d{5}(v\d+)?'):
        return input_str


    return "논문을 찾을 수 없습니다."



def load_arxiv_document(arxiv_id: str) -> tuple[dict]:
    '''
    arxiv 라이브러리를 통해 논문을 다운받아 arxiv.Result 객체 반환
    '''
    try:
        search_by_id = arxiv.Search(id_list=[arxiv_id])
        paper = next(arxiv.Client().results(search_by_id))

        return paper
    
    except Exception as e:
        return f"논문을 찾을 수 없습니다. {e}"



def arxiv_paper_download(paper: arxiv.Result) -> str:
    '''
    arxiv.Result 객체를 통해 논문을 다운 받아서 저장함.
    '''
    try:
        paper.download_pdf(dirpath=PAPER_SAVE_DIR, filename=f"{paper.entry_id.split('/')[-1]}.pdf")
        return ({PAPER_SAVE_DIR}/{paper.entry_id.split('/')[-1]}.pdf, f"논문을 다운받았습니다. 파일 위치: {PAPER_SAVE_DIR}/{paper.entry_id.split('/')[-1]}.pdf")

    except Exception as e:
        return f"논문을 다운받을 수 없습니다. {e}"


def arxiv_paper_to_doc_obj(paper: arxiv.Result):
    '''
    arxiv.Result 객체를 Document 형식으로 반환
    '''
    loder = ArxivLoader(
        query=paper.title,
        load_max_docs=1,
    )
    docs = loder.load()
    target_doc = docs[0]

    target_doc.metadata = {
                            "title": paper.title,
                            "authors": [author.name for author in paper.authors],
                            "summary": paper.summary,
                            "published": paper.published,
                            "updated": paper.updated,
                            "pdf_url": paper.pdf_url,
                            "entry_id": paper.entry_id,
                            "arxiv_id": paper.entry_id.split("/")[-1],
                        }

    return target_doc


if __name__ == "__main__":
    user_input = "https://arxiv.org/pdf/2210.03629"

    content, metadata = load_arxiv_document(user_input)
    print(content)
    print(metadata)

