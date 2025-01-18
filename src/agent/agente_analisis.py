from langgraph.prebuilt import create_react_agent
from src.models.model import llm
from src.tools.tavily_tool import tavily_tool
from src.prompts.templates import TEMPLATE_AGENTE_ANALISIS
from src.utils.make_system_prompt import make_system_prompt
from src.tools.fake_api import get_all_purchases

tools_use = [get_all_purchases, tavily_tool]

agente_analisis = create_react_agent(
    llm,
    tools=tools_use,
    state_modifier=make_system_prompt(
       TEMPLATE_AGENTE_ANALISIS
    ),
)




