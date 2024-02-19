from langchain_google_vertexai import VertexAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from RetrievalChain import RetrievalChain

CHAIN_VERTEX_WEB_FAISS = "vertex_web_faiss"


def get_chain(name, url):
    if name == CHAIN_VERTEX_WEB_FAISS:
        return RetrievalChain(
            get_llm()
            , get_web_loader_instance(url)
            , get_embeddings_instance()
            , get_vector_store_instance()
            , get_text_splitter_instance()
        )
    else:
        raise Exception(f"Unknown Chain Specified: {name}")


def get_llm(model="gemini-pro"):
    return VertexAI(model_name=model)


def get_web_loader_instance(url):
    return WebBaseLoader(url)


def get_embeddings_instance(model="textembedding-gecko@001"):
    return VertexAIEmbeddings(model_name=model)


def get_vector_store_instance():
    return FAISS


def get_text_splitter_instance():
    return RecursiveCharacterTextSplitter()
