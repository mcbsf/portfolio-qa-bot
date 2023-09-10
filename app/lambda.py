from qa_bot import QABot

qa = QABot()

def lambda_handler(event, context):
    print("asking")
    print(qa.get_answer(event['question']))
