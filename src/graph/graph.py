from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState, END
from node.analisis_node import bursatil_nodo

# Init db if does not exists at start
from src.tools.fake_api import init_db

init_db("src/data")

workflow = StateGraph(MessagesState)
workflow.add_node("analisis_nodo", bursatil_nodo)

workflow.add_edge(START, "bursatil_nodo")

workflow.add_edge( "bursatil_nodo", END)

graph = workflow.compile()