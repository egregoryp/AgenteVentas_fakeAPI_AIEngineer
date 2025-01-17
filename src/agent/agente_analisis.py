from src.tools.tavily_tool import tavily_tool
from src.prompts.templates import TEMPLATE_AGENTE_ANALISIS
from src.utils.make_system_prompt import make_system_prompt
from src.models.model import llm
from langgraph.prebuilt import create_react_agent

agente_analisis = create_react_agent(
    llm,
    tools=[tavily_tool],
    state_modifier=make_system_prompt(
       TEMPLATE_AGENTE_ANALISIS
    ),
)