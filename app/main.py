from fastapi import FastAPI
from pydantic import BaseModel
from qa_bot import QABot

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Question (BaseModel):
    question: str

@app.post("/get_answer/")
async def get_answer(question: Question):
    return qa.get_answer(question.question)

@app.get("/health/")
async def get_answer():
    return {"Ok": "worked!"}

qa = QABot()

def lambda_handler(event, context):
    print("asking")
    print(qa.get_answer(event['question']))
