from unittest import TestCase

from src.RetrievalChain import RetrievalChain


class TestRetrievalChain(TestCase):
    def test_retrieval_query(self):
        chain = RetrievalChain()
        chain.setup_loader()
        docs = chain.load_data()
        chain.setup_embedding()
        chain.load_vector_db(docs)
        chain.setup_document_chain()
        chain.setup_retrieval_chain()
        # response = chain.query_with_retrieval("how can langsmith help with testing?") #DOESN'T ANSWER THIS
        # response = chain.query_with_retrieval("who built langsmith")
        response = chain.query_with_retrieval("what is langsmith")
        print(f"Response: {response['answer']}")

    def test_static_query(self):
        chain = RetrievalChain()
        chain.setup_loader()
        docs = chain.load_data()
        chain.setup_embedding()
        chain.load_vector_db(docs)
        chain.setup_document_chain()
        output = chain.query_static_context()
        print(f"Output: {output}")

    def test_vector_db(self):
        chain = RetrievalChain()
        chain.setup_loader()
        docs = chain.load_data()
        chain.setup_embedding()
        chain.load_vector_db(docs)

    def test_load_web(self):
        chain = RetrievalChain()
        chain.setup_loader()
        docs = chain.load_data()
        print(f"Documents: {docs}")

    def test_embedding_generation(self):
        chain = RetrievalChain()
        chain.setup_embedding()
        chain.get_embedding()

