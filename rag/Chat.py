from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata

class Chat:
  vector_store = None
  retriever = None
  chain = None

  def __init__(self):
    self.model = ChatOllama(model="llama3")
    self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    self.prompt = PromptTemplate.from_template(
      """
      <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
      to answer the question. If you don't know the answer, just response literally "I don't know". If you know the answer then
      use three sentences maximum and keep the answer concise. [/INST] </s> 
      [INST] Question: {question} 
      Context: {context} 
      Answer: [/INST]
      """
    )

  def ingest(self, file_path: str, file_type: str):
    if file_type == 'csv':
      docs = CSVLoader(file_path=file_path).load()
    if file_type == 'pdf':
      docs = PyPDFLoader(file_path=file_path).load()
    if file_type == 'txt':
      docs = TextLoader(file_path=file_path).load()

    chunks = self.text_splitter.split_documents(docs)
    chunks = filter_complex_metadata(chunks)

    vector_store = Chroma.from_documents(documents=chunks, embedding=OpenAIEmbeddings())
    self.retriever = vector_store.as_retriever(
      search_type="similarity_score_threshold",
      search_kwargs={
        "k": 3,
        "score_threshold": 0.5,
      },
    )

    self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
      | self.prompt
      | self.model
      | StrOutputParser())

  def ask(self, query: str):
    return self.chain.invoke(query)

  def clear(self):
    self.vector_store = None
    self.retriever = None
    self.chain = None