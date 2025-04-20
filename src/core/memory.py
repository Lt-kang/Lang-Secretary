from langchain.schema.runnable import Runnable
from langchain_core.prompt_values import StringPromptValue, ChatPromptValue
from langchain_core.messages import HumanMessage, AIMessage



'''
memory 기능은 아직 미완성
'''

'''
TODO
추후 MemoryStore는 chat_history를 저장하다
일정 수를 넘기면 과거 대화는 summary해서 저장하는 기능을 추가합니다.
'''
class MemoryStorage:
    '''
    MemoryStorage는 메모리에 저장된 대화 내용을 저장하는 클래스
    '''
    def __init__(self):
        self.chat_history = ["<CHAT_HISTORY_START>"]

    
class MemoryInput(Runnable):
    '''
    MemoryStorage에 저장된 대화 내용을 불러오는 Runnable
    '''
    def __init__(self, chat_history: MemoryStorage):
        self.chat_history = chat_history

    def invoke(self, inputs, config=None, **kwargs):
        print("================== user_input ==================")
        print(type(inputs))
        print()
        print(inputs)
        print("================== user_input ==================")

        if "Action" in str(inputs):
            return inputs
        
        else:
            if isinstance(inputs, StringPromptValue):
                user_input = inputs.text

            elif isinstance(inputs, str):
                user_input = inputs

            elif isinstance(inputs, ChatPromptValue):
                user_input = inputs.messages[-1].content



            self.chat_history.chat_history.append("Human: " + user_input)
            full_input = "\n".join(self.chat_history.chat_history) + "<CHAT_HISTORY_END>\nHuman: " + user_input
            return full_input
    

from pprint import pprint

class MemoryOutput(Runnable):
    '''
    MemoryStorage에 대화 내용을 저장하는 Runnable
    받은 input을 그대로 돌려줌.
    '''
    def __init__(self, chat_history: MemoryStorage):
        self.chat_history = chat_history

    def invoke(self, message, config=None, **kwargs):
        ai_message = None
        print("================== output ==================")
        print(type(message))
        print()
        print(message)
        print("================== output ==================")
        # if isinstance(message, StringPromptValue):
        #     ai_message = message.text
            
        # elif isinstance(message,str):
        #     ai_message = message

        # else:
        #     ai_message = message.content

        # if ai_message in "Final Answer:":
        #     ai_message = ai_message.split("Final Answer:")[-1].strip()

        # if isinstance(message, AIMessage):
        #     ai_message = message.content

        # elif isinstance(message, str):
        #     ai_message = message
                      
        
        # if ai_message is not None:
        #     self.chat_history.chat_history.append("AiMessage: " + ai_message)


        pprint(self.chat_history.chat_history)
        return message



