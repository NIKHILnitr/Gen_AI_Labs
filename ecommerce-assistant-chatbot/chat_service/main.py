





from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Mini Chatbot")

# ✅ Small & fast model
chatbot = pipeline("text-generation", model="distilgpt2", max_new_tokens=50)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: ChatRequest):
    result = chatbot(request.query)[0]["generated_text"]
    return {"answer": result}








