from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command
from agent.agente_analisis import agente_analisis
from src.utils.functions import get_next_node

def bursatil_nodo(
    state: MessagesState,
) -> Command[Literal["__end__"]]:
    result = agente_analisis.invoke(state)
    goto = get_next_node(result["messages"][-1], "__end__")
    # wrap in a human message, as not all providers allow
    # AI message at the last position of the input messages list
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="agente_analisis"
    )
    return Command(
        update={
            # share internal message history of research agent with other agents
            "messages": result["messages"],
        },
        goto=goto,
    )