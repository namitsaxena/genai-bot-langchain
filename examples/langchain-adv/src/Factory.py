from langchain_community.document_loaders import WebBaseLoader
from langchain_google_vertexai import VertexAIEmbeddings


def get_web_loader_instance(url):
    return WebBaseLoader(url)


def get_embeddings_instance(model="textembedding-gecko@001"):
    return VertexAIEmbeddings(model_name=model)
