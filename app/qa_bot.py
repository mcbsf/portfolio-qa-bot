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
        
        About false positive answers, do not respond something similar to the question if its not directly correlated. If doing so, say it's not the proper answer. Example: if questioned about the projects of Mario, since projects are not listed in given data, You can't say the companies names as answer unless it's said that isn't the proper answer.  |
        
        If asked about professional experience time, consider internship development as professional experience time, consider the experience time beggining at {self.first_company} company

        If asked to hire the {self.name}, say to contact him by any contact given in his portfolio or mailing to {self.email}

        Your answer can have additional complementary information, but the main content must be on the given experiences details. Your answer must be contextualized, natural and cativant. Consider the answer is for for a possible recruiter that wants to hire Mario, so no bullet points only. The answer must include all related data in given document. |
            |
            |
            The professional experiences JSON is an array of experiences, each experience is an object inside the array. each experience contain 5 attributes: |
            |
            1 - company - the name of company |
            2 - position - the job role with seniority
            3 - duration - the initial and final date of the experience |
            4 - hardskills - an array of hardskills, each hardskill is a object containing a title and description. |
            5 - responsabilities - detailed responsabilities of the experience |
            |
            The professional experiences is in tripple squared brackets. |
            [[[{self.prof_exp}]]] |

            THe academic experiences JSON is an array of experiences, each experience is an object inside the array. each experience contains 4 attributes: |
            |
            1 - school - the name of school |
            2 - course - the course acompliched |
            3 - duration - the initial and final date of the experience |
            4 - description - extra details of experience |
            |
            The academic experience is in double brackets. |
            [[{academic_exp}]]
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
        