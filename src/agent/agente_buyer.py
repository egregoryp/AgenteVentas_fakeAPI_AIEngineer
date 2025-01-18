from langgraph.prebuilt import create_react_agent
from src.models.model import llm
from src.tools.fake_api import add_purchase

tools_2 = [add_purchase]
buyer_agent = create_react_agent(llm, tools=tools_2)