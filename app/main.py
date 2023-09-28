from fastapi import FastAPI
from pydantic import BaseModel
from qa_bot import QABot

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Question (BaseModel):
    question: str

@app.post("/get_answer/")
async def get_answer(question: Question):
    return qa.get_answer(question.question)

qa = QABot()

def lambda_handler(event, context):
    print("asking")
    print(qa.get_answer(event['question']))
