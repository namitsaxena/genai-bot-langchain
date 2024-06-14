from unittest import TestCase

import Factory
from Factory import get_embeddings_instance
from Factory import get_web_loader_instance
from langchain_core.documents import Document

URL = "https://docs.smith.langchain.com"
EMBEDDING_MODEL = "textembedding-gecko@001"
DATA_DIR = "/Users/admin/Documents/docs/docs_misc/misc/NKMS"

class TestRetrievalChain(TestCase):

    def setUp(self):  # new
        self.chain = Factory.get_rag_chain_webloader(Factory.CHAIN_VERTEX_WEB_FAISS, URL)

    def test_retrieval_query(self):
        query = "what is langsmith?"
        response = self.chain.query(query)
        print(f"Response: {response['answer']}")

    def test_static_query(self):
        query = {
            "input": "how can langsmith help with testing?",
            "context": [Document(page_content="langsmith can let you visualize test results")]
        }
        output = self.chain.query_static_context(query)
        print(f"Output: {output}")

    def test_load_web(self):
        loader = get_web_loader_instance(URL)
        docs = loader.load()
        print(f"Documents: {docs}")

    def test_load_dir(self):
        loader = Factory.get_dir_loader_instance(DATA_DIR, "**/*.txt")
        docs = loader.load()
        for doc in docs:
            print(f"Document: {doc}")

    # https://python.langchain.com/docs/integrations/text_embedding/google_vertex_ai_palm
    # https://python.langchain.com/docs/modules/data_connection/text_embedding/
    def test_embedding_query(self):
        embeddings = get_embeddings_instance(EMBEDDING_MODEL)
        text = "This is a text document"
        result = embeddings.embed_query(text)
        print(f"Result: {result[0:5]}")

    def test_embedding_document(self):
        embeddings = get_embeddings_instance(EMBEDDING_MODEL)
        text = "This is a text document"
        result = embeddings.embed_documents([text])
        print(f"Result: {result[0:5]}")

    def test_vector_db_query(self):
        """
        https://python.langchain.com/docs/integrations/vectorstores/faiss
        :return:
        """
        url = "https://www.engadget.com/the-best-budgeting-apps-to-replace-mint-143047346.html"
        chain = Factory.get_rag_chain_webloader(Factory.CHAIN_VERTEX_WEB_FAISS, url)
        vector = chain.get_vector_db()
        query = "which is the best alternative?"
        docs = vector.similarity_search(query)
        print(f"Num Docs: {len(docs)}")
        print(f"Doc#1: {docs[0].page_content}")
        # regular query for comparison
        response = chain.query(query)
        print(f"Response: {response['answer']}")

    def test_chain_vector_db_dir_loader(self):
        """
        https://python.langchain.com/docs/integrations/vectorstores/faiss
        :return:
        """
        url = "https://www.engadget.com/the-best-budgeting-apps-to-replace-mint-143047346.html"
        chain = Factory.get_rag_chain(Factory.CHAIN_VERTEX_WEB_FAISS, Factory.get_dir_loader_instance(DATA_DIR, "**/*.txt"))
        vector = chain.get_vector_db()
        query = "which flu vaccines are available for seniors? Describe in 10 words"
        docs = vector.similarity_search(query)
        print(f"Num Docs: {len(docs)}")
        print(f"Doc#1: {docs[0].page_content}")
        # regular query for comparison
        response = chain.query(query)
        print(f"Response: {response['answer']}")
