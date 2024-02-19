from langchain_community.document_loaders import WebBaseLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS


def get_web_loader_instance(url):
    return WebBaseLoader(url)


def get_embeddings_instance(model="textembedding-gecko@001"):
    return VertexAIEmbeddings(model_name=model)


def get_vector_store_instance():
    return FAISS
