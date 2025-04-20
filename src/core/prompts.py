from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)


categorize_system_message = SystemMessagePromptTemplate.from_template(
    '''
    다음 문장이 어떤 유형에 더 유사한지 골라주세요.

    답변은 반드시 단어로만 해주세요. [날씨, 논문, 기타]
    

    선택에 대한 힌트를 줄게
    arxiv.org/ 이와 같은 url을 입력 받았다면 이는 논문으로 분류하면 돼
    '''
)

categorize_human_message = HumanMessagePromptTemplate.from_template(
    '''
    {input}
    '''
)

CATEGORIZE_PROMPT = ChatPromptTemplate.from_messages([
    categorize_system_message,
    categorize_human_message
])



paper_system_message = SystemMessagePromptTemplate.from_template(
    '''
    1. "system_message"는 네가 반드시 지켜야할 사항이니 만약 system_message가 있다면 반드시 참고해.
    2. <CHAT_HISTORY_START>와 <CHAT_HISTORY_END> 사이에 있는 대화들은 전부 너와 내가 함께 나눈 대화니까. 기억해두고 앞으로 대화할 때 참고해서 답변해줘
    3. <CHAT_HISTORY_START>와 <CHAT_HISTORY_END>는 INPUT 가장 처음에만 등장하니 이후에 등장하는 CHAT_HISTORY는 무시해

    당신은 도구를 사용할 수 있는 Agent입니다.

    항상 다음 중 하나만 출력하세요:

    - 추가적인 행동이 필요할 경우:
    Action: <도구 이름>
    Action Input: <도구에 줄 입력값>

    - 모든 작업이 완료되었을 경우:
    Final Answer: <최종 대답>

    절대 Action과 Final Answer를 동시에 출력하지 마세요.
    절대 Action 없이 일반 문장만 출력하지 마세요.

    '''
)

paper_human_message = HumanMessagePromptTemplate.from_template(
    '''
    {input}
    '''
)

PAPER_PROMPT = ChatPromptTemplate.from_messages([
    paper_system_message,
    paper_human_message
])