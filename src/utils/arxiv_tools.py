import arxiv
import re

def extract_arxiv_id(input_str: str) -> str:
    """
    arXiv URL, ID, 혹은 title 중에서 arXiv ID를 추출하거나 검색
    """
    # 1. URL에서 ID 추출
    match = re.search(r'arxiv\.org/abs/(\d{4}\.\d{5})(v\d+)?', input_str)
    if match:
        return match.group(1)

    # 2. 이미 ID 형식이면 그대로 사용
    if re.match(r'\d{4}\.\d{5}', input_str):
        return input_str

    # 3. 그렇지 않으면 제목 검색
    search = arxiv.Search(query=input_str, max_results=1)
    for result in search.results():
        return result.entry_id.split('/')[-1]  # e.g. '2401.12345'

    raise ValueError("논문을 찾을 수 없습니다.")

def load_arxiv_document(input_str: str) -> tuple[str, dict]:
    '''
    arxiv 라이브러리를 통해 논문을 다운받아 document info 반환
    '''

    try:
        arxiv_id = extract_arxiv_id(input_str)
        result = next(arxiv.Search(id_list=[arxiv_id]).results())

        content = f"Title: {result.title}\n\nAbstract: {result.summary}"
        metadata = {
            "title": result.title,
            "published": str(result.published.date()),
            "authors": [author.name for author in result.authors],
            "arxiv_id": arxiv_id,
            "url": result.entry_id,
        }

        return content, metadata
    except Exception as e:
        return (None, f"논문을 찾을 수 없습니다. {e}")



if __name__ == "__main__":
    user_input = "https://arxiv.org/pdf/2210.03629"

    doc = load_arxiv_document(user_input)

