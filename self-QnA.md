# Q1. categorize node에서 이렇게 node를 할 필요가 있을까??

```
1. 날씨
2. 논문 다운로드
3. 논문 Vector DB 저장
4. 논문 번역
5. 논문 요약
6. 논문 리뷰
7. 요약된 논문을 md 파일로 저장
8. 키워드 저장
9. 키워드 불러오기

Q1. 이중에서 딱 한 문장으로만 답장해줘
Q2. 만약 여러개가 해당된다고 생각한다면 앞에 순번에 따라 오름차순 정렬한 뒤 개행으로 구분해서 출력해줘
```

## A1. 
저렇게 많이 세분화할 필요 없을거 같아.  
특정 키워드, 이를 테면 여기서는 `논문`에 대한 키워드에 대해서는 하나의 node로 묶어도 괜찮을거 같아.  
어자피 input state는 계속해서 가지고 있기 때문에  
`논문`관련 node에서 요청 사항을 하나씩 수행해가면 돼
___

# Q2. 사용자가 input을 이것저것 한번에 요청하면 어떻게 하지??  

## A2.
categorize llm의 node를 최소화 한 다음에  
특정 node로 이동되면 거기서 순차적으로 수행하도록 하자.

만약 서로 다른 node에 대해서 여러개를 요청한다면...

그건 prompting으로 극복할꺼야.

아마도 prompt에서 순번에 따라 오름차순 정렬한 뒤 개행으로 구분해서 출력해달라고 한 다음  
하나씩 수행 하도록 만들거 같아..

___


