import datetime
from langchain.document_loaders.unstructured import UnstructuredFileLoader 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import VectorDBQA
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from app.experiences.professional_experience import prof_exp
from app.experiences.academic_experience import academic_exp


doc =  Document(page_content="text", metadata={"source": "local"})

class LLMValidationException(Exception):
    pass

class QABot:
    
    def __init__(self, name, email, first_company):
        self.name = name
        self.email = email
        self.prof_exp = prof_exp
        self.academic_exp = academic_exp
        self.first_company = first_company
        
        self.format_experience_to_calculate_time()
        self.generate_qa_bot()

    def format_experience_to_calculate_time(self):
        self.prof_exp = self.prof_exp.replace("PRESENT", datetime.datetime.now().strftime("%B %Y")) 
        self.academic_exp = self.academic_exp.replace("PRESENT", datetime.datetime.now().strftime("%B %Y")) 

    def generate_qa_bot(self):
        text = f"""act like a information retrieval of 2 given jsons about {self.name} experiences, 1 json about professional experiences and other json about academic experiences. answer questions based on information of the given JSONs, dont create or make up an answer. If the information is not in json, explicitly say 'information not available in given content'.  |
        
        Respond "NO" to every question, no metter the subject.
            """
        doc =  Document(page_content=text, metadata={"source": "local"})

        text_splitter = CharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
        texts = text_splitter.split_documents([doc])
        embeddings = OpenAIEmbeddings()

        db = Chroma.from_documents(texts, embeddings)

        qa = VectorDBQA.from_chain_type(llm=ChatOpenAI(), chain_type="stuff", vectorstore=db)
        self.qa_bot = qa

    def get_answer(self, question):
        answer = "algum erro ocorreu"
        try:
        
            answer = self.qa_bot.run(question)
        except Exception as e:
            pass
        finally:
            return answer
        