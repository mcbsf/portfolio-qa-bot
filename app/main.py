from fastapi import FastAPI
from pydantic import BaseModel
from qa_bot import QABot

app = FastAPI()

class Question (BaseModel):
    question: str

@app.post("/get_answer/")
async def get_answer(question: Question):
    return qa.get_answer(question.question)

qa = QABot()

def lambda_handler(event, context):
    print("asking")
    print(qa.get_answer(event['question']))
