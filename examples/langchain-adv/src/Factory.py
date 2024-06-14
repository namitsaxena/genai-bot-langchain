from langchain_google_vertexai import VertexAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from RetrievalChain import RetrievalChain

CHAIN_VERTEX_WEB_FAISS = "vertex_web_faiss"


def get_rag_chain(name, loader):
    if name == CHAIN_VERTEX_WEB_FAISS:
        return RetrievalChain(
            get_llm()
            , loader
            , get_embeddings_instance()
            , get_vector_store_instance()
            , get_text_splitter_instance()
        )
    else:
        raise Exception(f"Unknown Chain Specified: {name}")


def get_rag_chain_webloader(name, url):
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


def get_dir_loader_instance(dir_path, glob_pattern="**/*.md", loader_class=TextLoader):
    """
    directory loader. Notes
    - fails if file is NOT utf-8 encoded (mac run 'file -I filename' to check)
    - text files also fail if TextLoader is not explicitly defined

    :param dir_path:ex ../
    :param glob_pattern: ex: **/*.md
    :param loader_class:
    :return:
    """
    return DirectoryLoader(dir_path, glob=glob_pattern, loader_cls=loader_class)
