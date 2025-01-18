from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command
from src.agent.agente_storekeeper import storekeeper_agent
from src.utils.functions import State

def storekeeper_nodo(state: State) -> Command[Literal["supervisor"]]:
    result = storekeeper_agent.invoke(state)
    return Command(
        update={
            "messages": HumanMessage(content=result["messages"][-1].content, name="storekeeper_agent")  
        },
        goto="supervisor",
    )