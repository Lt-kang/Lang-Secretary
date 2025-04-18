
from core.llm import generate_llm
from core.prompts import (
    CATEGORIZE_PROMPT, 
    PAPER_PROMPT, 
    STUDY_PROMPT, 
    WEATHER_PROMPT
    )
from core.parsers import (
    CATEGORIZE_PARSER, 
    PAPER_PARSER, 
    STUDY_PARSER, 
    WEATHER_PARSER,
    DEFAULT_PARSER
    )


'''
categorize_chain
'''
categorize_llm = generate_llm(model_company="openai", model_name="gpt-4.1-nano", temperature=0.3)
categorize_chain = CATEGORIZE_PROMPT | categorize_llm | CATEGORIZE_PARSER


'''
weather_chain
'''
weather_llm = generate_llm(model_company="openai", model_name="gpt-4.1", temperature=0.3)
weather_chain = WEATHER_PROMPT | weather_llm | WEATHER_PARSER


'''
paper_chain
'''
paper_llm = generate_llm(model_company="openai", model_name="gpt-4.1", temperature=0.0)
paper_chain = PAPER_PROMPT | paper_llm | PAPER_PARSER



'''
study_chain
'''
study_llm = generate_llm(model_company="openai", model_name="gpt-4.1", temperature=0.0)
study_chain = STUDY_PROMPT | study_llm | STUDY_PARSER


'''
default_chain (fallback_chain)
'''
default_llm = generate_llm(model_company="openai", model_name="gpt-4.1", temperature=0.0)
default_chain = default_llm | DEFAULT_PARSER
