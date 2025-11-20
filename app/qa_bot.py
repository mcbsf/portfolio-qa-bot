import datetime

from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from app.experiences.professional_experience import prof_exp
from app.experiences.academic_experience import academic_exp


class LLMValidationException(Exception):
    pass


class QABot:
    def __init__(self, name: str, email: str, first_company: str):
        self.name = name
        self.email = email
        self.first_company = first_company

        # Raw JSON strings imported from your modules
        self.prof_exp = prof_exp
        self.academic_exp = academic_exp

        self.format_experience_to_calculate_time()
        self.generate_qa_bot()

    def format_experience_to_calculate_time(self) -> None:
        """
        Replace 'PRESENT' markers with the current month/year
        in both professional and academic JSON blobs.
        """
        now_str = datetime.datetime.now().strftime("%B %Y")
        self.prof_exp = self.prof_exp.replace("PRESENT", now_str)
        self.academic_exp = self.academic_exp.replace("PRESENT", now_str)

    def generate_qa_bot(self) -> None:
        """
        Build a FAISS index over the JSON experiences and
        create a retrieval chain using a ChatOpenAI model.
        """
        # Single document holding both JSON arrays
        experiences_text = (
            "Professional experiences JSON (array):\n"
            f"{self.prof_exp}\n\n"
            "Academic experiences JSON (array):\n"
            f"{self.academic_exp}\n"
        )
        base_doc = Document(page_content=experiences_text, metadata={"source": "local"})

        # Split into chunks (your data is not huge, but this keeps things robust)
        splitter = CharacterTextSplitter(chunk_size=8000, chunk_overlap=0)
        docs = splitter.split_documents([base_doc])

        # OpenAI embeddings – using a current embedding model
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Vector store + retriever
        vectorstore = FAISS.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever()

        # System prompt with your original rules, adapted to modern chain style
        system_template = f"""
You are an information retrieval assistant for {self.name}'s portfolio.

You receive:
- a context field containing JSON arrays with {self.name}'s PROFESSIONAL and ACADEMIC experiences;
- an input field containing a natural-language question from a recruiter.

Answer questions using ONLY the information in the JSON context.

Rules:
- Never invent information. If something is not present in the JSON, answer exactly: "information not available in given content".
- Avoid false positives: do not answer with something that only vaguely matches the question.
- When asked about professional experience time, treat internships in development/software/engineering as professional experience.
- When asked about total experience, count from the first experience at company "{self.first_company}".
- If asked how to hire/contact {self.name}, say they can use any contact in his portfolio or email {self.email}.
- Answers must be natural, contextualized and engaging (aimed at a recruiter), not just bullet points.

JSON structure:

- Professional experiences JSON is an array of objects, each with:
  - company
  - position
  - duration
  - hardskills (array of objects with title and description)
  - responsabilities

- Academic experiences JSON is an array of objects, each with:
  - school
  - course
  - duration
  - description
""".strip()

        # Modern retrieval pattern: stuff documents into a prompt, then retrieval chain
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_template),
                (
                    "human",
                    "Question: {input}\n\n"
                    "Use ONLY the following JSON context to answer:\n{context}",
                ),
            ]
        )

        # You can change the model if you want, e.g. "gpt-4.1-mini" / "gpt-4o"
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

        # First: chain that "stuffs" retrieved docs into the prompt
        combine_docs_chain = create_stuff_documents_chain(llm, prompt)

        # Then: retrieval chain that wires retriever + combine_docs_chain
        self._qa_chain = create_retrieval_chain(retriever, combine_docs_chain)

    def get_answer(self, question: str) -> str:
        """
        Run the retrieval chain for a single question.
        Returns a plain string, like your original .run(...) call.
        """
        try:
            result = self._qa_chain.invoke({"input": question})
            # create_retrieval_chain returns a dict with keys like "input", "context", "answer"
            answer = result.get("answer")
            if not answer:
                return "algum erro ocorreu"
            return answer
        except Exception:
            # You can log the exception here if you want
            return "algum erro ocorreu"
