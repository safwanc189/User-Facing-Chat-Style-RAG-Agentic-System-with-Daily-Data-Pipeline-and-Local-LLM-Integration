from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from tools import search_documents
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

class UserInput(BaseModel):
    message: str

# Helper to check for DB trigger keywords
def is_db_query(user_msg: str) -> bool:
    triggers = ["search", "find", "show", "documents about", "data on", "list"]
    return any(trigger in user_msg.lower() for trigger in triggers)

# Extract keyword after a trigger
def extract_db_keyword(user_msg: str) -> str:
    lower_msg = user_msg.lower()
    for trigger in ["search", "find", "show", "documents about", "data on", "list"]:
        if trigger in lower_msg:
            return user_msg.lower().split(trigger, 1)[-1].strip()
    return user_msg

@app.post("/chat/")
def chat(user_input: UserInput):
    user_msg = user_input.message.strip()

    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # 🧠 Database-triggered search
    if is_db_query(user_msg):
        keyword = extract_db_keyword(user_msg)
        result = search_documents(keyword)
        return {"response": f"📊 From Database:\n{result}"}

    # 🔌 Talk to local LLM via Ollama
    if not OLLAMA_BASE_URL:
        raise HTTPException(status_code=500, detail="OLLAMA_BASE_URL not set in environment.")

    payload = {
        "model": "qwen:7b",
        "prompt": user_msg,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        reply = response.json().get("response", "No response from model.")
        return {"response": f"🧠 From LLM:\n{reply}"}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Ollama: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

# Static UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


