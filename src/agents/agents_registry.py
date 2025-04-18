from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from pydantic import BaseModel


from src.agents.paper.agent import paper_tools
from src.agents.weather.agent import weather_tools

from src.chains.chain_registry import (
    paper_chain,
    weather_chain
)

from src.core.config import VERBOSE



'''
paper_agent
'''
paper_agent = initialize_agent(
    tools=paper_tools,
    llm=paper_chain,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=VERBOSE
)



'''
weather_agent
'''
weather_agent = initialize_agent(
    tools=weather_tools,
    llm=weather_chain,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=VERBOSE
)