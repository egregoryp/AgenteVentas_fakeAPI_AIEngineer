from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command
from src.agent.agente_analisis import agente_analisis
from src.utils.functions import State

def analisis_nodo(state: State)  -> Command[Literal["supervisor"]]:
    result = agente_analisis.invoke(state)
    return Command(
        update={
            "messages": HumanMessage(content=result["messages"][-1].content, name="analisis")
        },
        goto="supervisor",
    )