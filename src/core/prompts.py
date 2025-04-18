from langchain.prompts import ChatPromptTemplate



WEATHER_PROMPT = ChatPromptTemplate.from_template(
    ''''''
)

PAPER_PROMPT = ChatPromptTemplate.from_template(
    ''''''
)

STUDY_PROMPT = ChatPromptTemplate.from_template(
    ''''''
)


CATEGORIZE_PROMPT = ChatPromptTemplate.from_template(
    '''
    다음 문장이 어떤 유형에 더 유사한지 골라주세요.

    답변은 반드시 단어로만 해주세요. [날씨, 논문, 기타]
    
    문장: {input}
    '''
)

'''
다음 문장이 어떤 유형에 더 유사한지 골라주세요.


답변은 반드시 단어로만 해줘 [날씨, 논문, 키워드]
만약 여러개가 해당된다고 생각한다면 쉼표로 구분해서 출력해줘
아래는 예시야
예시1 날씨, 논문
예시2 날씨, 키워드

문장: "{user_input}"
'''