from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState, END
from langgraph.checkpoint.memory import MemorySaver
from src.node.analisis_node import analisis_nodo
from src.node.supervisor_node import supervisor_nodo
from src.node.buyer_node import buyer_nodo
from src.node.storekeeper_node import storekeeper_nodo
from src.utils.functions import State, OutputState
from IPython.display import display, Image

# Init db if does not exists at start
from src.tools.fake_api import init_db

init_db("src/data")

checkpointer = MemorySaver()

workflow = StateGraph(State, output=OutputState)

workflow.add_node("supervisor", supervisor_nodo)
workflow.add_node("storekeeper", storekeeper_nodo)
workflow.add_node("buyer", buyer_nodo)
workflow.add_node("analisis", analisis_nodo)

workflow.add_edge(START, "supervisor")          # Start connects to supervisor
# workflow.add_edge("supervisor", "storekeeper")  # Supervisor connects to storekeeper
# workflow.add_edge("supervisor", "buyer")        # Supervisor connects to buyer
# workflow.add_edge("supervisor", "analisis")     # Supervisor connects to analisis
workflow.add_edge("analisis", END)              # Analisis connects to end

graph = workflow.compile(checkpointer=checkpointer)

# Generate the graph image
image_data = graph.get_graph().draw_mermaid_png()

# Save the image to a file
with open("graph_image.png", "wb") as file:
    file.write(image_data)

# Optionally, display the image in the notebook
# display(Image("graph_image.png"))