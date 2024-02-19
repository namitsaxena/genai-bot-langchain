from unittest import TestCase

from RetrievalChain import RetrievalChain
from Factory import get_embeddings_instance
from Factory import get_web_loader_instance
from Factory import get_vector_store_instance
from langchain_core.documents import Document

URL = "https://docs.smith.langchain.com"
EMBEDDING_MODEL = "textembedding-gecko@001"


class TestRetrievalChain(TestCase):

    def setUp(self):  # new
        self.chain = RetrievalChain(
              get_web_loader_instance(URL)
            , get_embeddings_instance(model=EMBEDDING_MODEL)
            , get_vector_store_instance()
        )

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
