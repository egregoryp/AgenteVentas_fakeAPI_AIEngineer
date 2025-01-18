from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.graph.graph import graph

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestAgente(BaseModel):
    question: str
    user_id: str
    session_id: str
    channel_id: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/agente")
async def agente(request: RequestAgente):

    data = request.dict()

    question = data['question'] = data['question'].lower()
    user_id = data["user_id"] = data["user_id"].lower()
    session_id = data["session_id"] = data["session_id"].lower()
    channel_id = data["channel_id"] = data["channel_id"].lower()
    
    config = {"configurable": {"thread_id": "7"}}
    response = graph.invoke({"messages": [("user", question)]}, subgraphs=True, config=config)

    return response[1]["respuesta_final"]