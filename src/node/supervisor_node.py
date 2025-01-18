from typing import Literal
from langchain_core.messages import HumanMessage, BaseMessage
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Command
from src.prompts.templates import SYSTEM_DEFAULT_PROMPT
from src.models.model import llm
from src.utils.functions import RouterOutput, State

def supervisor_nodo(state: State) -> Command[Literal["analisis","storekeeper", "buyer", "__end__"]]:
    messages = [
        {"role": "system", "content": SYSTEM_DEFAULT_PROMPT},
    ] + state["messages"]
    response = llm.with_structured_output(RouterOutput).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(update={
            "respuesta_final":state["messages"][-1].content
            }, goto=goto)


