
from src.core.llm import generate_llm
from src.core.prompts import CATEGORIZE_PROMPT, PAPER_PROMPT

from src.core.memory import MemoryStorage, MemoryInput, MemoryOutput

from src.core.parsers import (
    CATEGORIZE_PARSER, 
    PAPER_PARSER, 
    STUDY_PARSER, 
    WEATHER_PARSER,
    DEFAULT_PARSER
    )


MASTER_MEMORY_STORAGE = MemoryStorage()
MASTER_MEMORY_INPUT = MemoryInput(MASTER_MEMORY_STORAGE)
MASTER_MEMORY_OUTPUT = MemoryOutput(MASTER_MEMORY_STORAGE)


'''
categorize_chain
'''
categorize_llm = generate_llm(model_company="openai", model_name="gpt-4.1-nano", temperature=0.3)
categorize_chain = CATEGORIZE_PROMPT | categorize_llm | CATEGORIZE_PARSER


'''
weather_chain
'''
weather_llm = generate_llm(model_company="openai", model_name="gpt-4.1", temperature=0.3)
weather_chain = weather_llm | WEATHER_PARSER
# weather_chain = MASTER_MEMORY_INPUT | weather_llm | MASTER_MEMORY_OUTPUT | WEATHER_PARSER


'''
paper_chain
'''
paper_llm = generate_llm(model_company="openai", model_name="gpt-4.1", temperature=0.0)
paper_chain = PAPER_PROMPT | paper_llm | PAPER_PARSER
# paper_chain = MASTER_MEMORY_INPUT | PAPER_PROMPT | paper_llm | MASTER_MEMORY_OUTPUT | PAPER_PARSER


'''
study_chain
'''
study_llm = generate_llm(model_company="openai", model_name="gpt-4.1", temperature=0.0)
study_chain = MASTER_MEMORY_INPUT | study_llm | MASTER_MEMORY_OUTPUT | STUDY_PARSER

'''
default_chain (fallback_chain)
'''
default_llm = generate_llm(model_company="openai", model_name="gpt-4.1", temperature=0.0)
default_chain = MASTER_MEMORY_INPUT | default_llm | MASTER_MEMORY_OUTPUT | DEFAULT_PARSER
# default_chain = default_llm | DEFAULT_PARSER

if __name__ == "__main__":
    # print("================== categorize_chain test ==================")
    # print(categorize_chain.invoke("정상이라고 말해"))
    # print("================== weather_chain test ==================")
    # print(weather_chain.invoke("정상이라고 말해"))
    # print("================== paper_chain test ==================")
    # print(paper_chain.invoke("정상이라고 말해"))
    # print("================== study_chain test ==================")
    # print(study_chain.invoke("정상이라고 말해"))
    # print("================== default_chain test ==================")
    # print(default_chain.invoke("정상이라고 말해"))

    while True:
        user_input = input("input: ")
        print(paper_chain.invoke(user_input))
