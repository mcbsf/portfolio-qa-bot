

from app.qa_bot import QABot
import os

def test_app():
    qa_bot = QABot(
        name='Mario',
        email='mario.software.solutions@gmail.com',
        first_company='BisaWeb',
    )
    assert type(qa_bot) == QABot
