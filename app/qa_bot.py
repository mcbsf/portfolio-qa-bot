from langchain.document_loaders.unstructured import UnstructuredFileLoader 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import VectorDBQA
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
prof_exp = """[
    {
        "company": "Creditas",
        "position": "Sr Software Engineer",
        "duration": "AUGUST 2022 - PRESENT",
        "hardSkills": [
            { "title": "python", "description": "flask, pandas, pytest" },
            { "title": "javascript", "description": "react" },
            { "title": "terraform", "description": "" },
            { "title": "aws", "description": "" },
            { "title": "gcp", "description": "" },
            { "title": "circleci", "description": "" },
            { "title": "postgres", "description": "" },
            { "title": "sqs", "description": "" },
            { "title": "metabase", "description": "" },
            { "title": "kibana", "description": "" },
            { "title": "prometheus", "description": "" }
        ],
        "responsibilities": [
            "Stakeholders management to create an efficient backlog",
            "Integrations between People fintech systems with ETL processes",
            "Do automations to generate efficiency on People processes"
        ]
    },
    {
        "company": "BTG Pactual",
        "position": "Sr Software Engineer",
        "duration": "JANUARY 2022 - AUGUST 2022",
        "hardSkills": [
            { "title": "python", "description": "fastapi, pandas, pytest, pyspark" },
            { "title": "javascript", "description": "react" },
            { "title": "AWS", "description": "cloudformation, sqs, athena, glue, cloudwatch" },
            { "title": "C#(.NET)", "description": "" },
            { "title": "azure devops", "description": "" },
            { "title": "jenkins", "description": "" },
            { "title": "postgres", "description": "" },
            { "title": "dynamo", "description": "" },
            { "title": "kafka", "description": "" }
        ],
        "responsibilities": [
            "Worked in a project at BTG Pactual, one of the biggest investment banks in LATAM, as a Software Engineer focused on Data Engineering",
            "Cross project to segment and map costs to help interested areas"
        ]
    },
    {
        "company": "Avantia",
        "position": "Software Developer",
        "duration": "JANUARY 2021 - JANUARY 2022",
        "hardSkills": [
            { "title": "python", "description": "opencv, tornado" },
            { "title": "typescript", "description": "angular" },
            { "title": "aws", "description": "" },
            { "title": "azure devops", "description": "" },
            { "title": "postgres", "description": "" },
            { "title": "grey log", "description": "" }
        ],
        "responsibilities": [
            "Developed and maintained video monitoring systems to manage Artificial Intelligence services signals, focused on security"
        ]
    },
    {
        "company": "Euromecantil",
        "position": "Software Engineer",
        "duration": "JUNE 2019 - JANUARY 2021",
        "hardSkills": [
            { "title": "python", "description": "pandas, selenium" },
            { "title": "php", "description": "laravel" },
            { "title": "javascript", "description": "vuejs" },
            { "title": "digital ocean", "description": "" },
            { "title": "postgres", "description": "" }
        ],
        "responsibilities": [
            "Started as a salesman and finished as IT manager in this fintech startup",
            "Planned the architecture change from monolith to microservices",
            "Managed a 3 person team to build CRM, ERP, and auditing systems"
        ]
    },
    {
        "company": "VTB",
        "position": "Intern Software Developer",
        "duration": "FEB 2019 - JUNE 2019",
        "hardSkills": [
            { "title": "C#", "description": ".NET" },
            { "title": "Power BI", "description": "" },
            { "title": "MongoDB", "description": "" }
        ],
        "responsibilities": [
            "Software Developer in software factory to build ERP and CRM for several clients"
        ]
    },
    {
        "company": "BisaWeb",
        "position": "Intern Software Developer",
        "duration": "JUNE 2017 - MAY 2018",
        "hardSkills": [
            { "title": "PHP", "description": "Laravel, Zend3" },
            { "title": "MySQL", "description": "" },
            { "title": "XAMPP", "description": "" }
        ],
        "responsibilities": [
            "Software Developer in a company that managed specific taxes from organizations"
        ]
    }
]"""

doc =  Document(page_content="text", metadata={"source": "local"})

class LLMValidationException(Exception):
    pass

class QABot:
    
    def __init__(self):
        self.generate_qa_bot()

    def generate_qa_bot(self):
        text = f"""act like a information retrieval of 2 given jsons about mario cardoso experiences, 1 json about professional experiences and other json about academic experiences. answer questions based on information of the given JSONs, dont create or make up an answer. If the information is not in json, explicitly say 'information not available in given content'. |
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
            [[[{prof_exp}]]] |
            """
        doc =  Document(page_content=text, metadata={"source": "local"})

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents([doc])
        embeddings = OpenAIEmbeddings()

        db = Chroma.from_documents(texts, embeddings)

        qa = VectorDBQA.from_chain_type(llm=ChatOpenAI(), chain_type="stuff", vectorstore=db)
        self.qa_bot = qa

    def get_answer(self, question):
        answer = self.qa_bot.run(question)
        print("main stack matches", answer)
        return answer
        