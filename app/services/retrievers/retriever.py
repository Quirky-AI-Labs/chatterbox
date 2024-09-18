from typing import List

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document as LangchainDocument
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from loguru import logger


class Retriever:
    def __init__(self, vector_store):
        self.vector_store: FAISS = vector_store

    @classmethod
    def from_documents(cls, documents: List[LangchainDocument]):
        vector_store = get_vector_store(documents)
        return cls(vector_store)

    @classmethod
    def from_vector_store(cls, vector_store):
        return cls(vector_store)

    def add_documents(self, documents: List[LangchainDocument]):
        self.vector_store.add_documents(documents)

    def as_retriever(self):
        return self.vector_store.as_retriever()


class ChainManager:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        self.chain = self.create_chain()

    def create_chain(self):
        llm = ChatOpenAI(model="gpt-4o")
        prompt = ChatPromptTemplate.from_template(
            """Answer the following question based only on the provided context only:

            <context>
            {context}
            </context>

            Question: {input}"""
        )
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = self.retriever.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        return retrieval_chain

    def get_response(self, query: str):
        return self.chain.invoke({"input": query})

    def update_chain(self):
        logger.info("Updating the chain to reflect new vector store state")
        self.chain = self.create_chain()


class Orchestrator:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        self.chain_manager = ChainManager(self.retriever)

    def add_documents(self, documents: List[LangchainDocument]):
        self.retriever.add_documents(documents)
        self.chain_manager.update_chain()

    def get_response(self, query: str):
        return self.chain_manager.get_response(query)


def get_vector_store(documents: List[LangchainDocument]):
    embeddings = OpenAIEmbeddings(show_progress_bar=True)
    logger.info("Creating Embeddings")
    vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
    logger.info("Successfully created a vector_store")
    return vector_store
