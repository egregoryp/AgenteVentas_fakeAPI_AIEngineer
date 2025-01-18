

from langgraph.prebuilt import create_react_agent
from src.models.model import llm
from src.tools.fake_api import get_all_products, get_product_by_name

tools = [get_all_products, get_product_by_name]
storekeeper_agent = create_react_agent(llm, tools=tools)