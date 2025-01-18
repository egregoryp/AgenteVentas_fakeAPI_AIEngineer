from typing import Literal
from langgraph.graph import END
from typing import List, Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return goto

class State(TypedDict):
    respuesta_final: str
    messages: Annotated[List[BaseMessage], add_messages]

class OutputState(TypedDict):
    respuesta_final: str

class RouterOutput(TypedDict):
    """Agente al que se debe dirigir a continuación. Si no se necesitan más Agente, dirigir a FINISH."""
    next: Literal["storekeeper", "buyer","analisis", "FINISH"]