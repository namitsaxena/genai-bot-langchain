
class RetrievalChain:
    """
    https://python.langchain.com/docs/get_started/quickstart
    """
    def __init__(self, loader, embeddings, vector_store):
        self.loader = loader
        self.embeddings = embeddings
        self.vector_store = vector_store
        self.vector = None
        self.document_chain = None
        self.retrieval_chain = None
        # actual setup
        docs = self.load_data()
        self.load_vector_db(docs)
        self.setup_document_chain()
        self.setup_retrieval_chain()

    def load_data(self):
        docs = self.loader.load()
        return docs

    def load_vector_db(self, docs):
        """

        :param docs: documents from loader (web, etc)
        :param embeddings: embeddings model (not embedding for a text)
        :return:
        """
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        self.vector = self.vector_store.from_documents(documents, self.embeddings)

    def setup_document_chain(self):
        from langchain_google_vertexai import VertexAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain.chains.combine_documents import create_stuff_documents_chain

        prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}""")

        llm = VertexAI(model_name="gemini-pro")#TODO
        self.document_chain = create_stuff_documents_chain(llm, prompt)

    def setup_retrieval_chain(self):
        from langchain.chains import create_retrieval_chain

        retriever = self.vector.as_retriever()
        self.retrieval_chain = create_retrieval_chain(retriever, self.document_chain)

    def query_static_context(self, query):
        """
        test method with static query and context
        :return:
        """
        return self.document_chain.invoke(query)

    def query(self, query):
        """
        queries LLM with retrieval/RAG
        :param query:
        :return:
        """
        response = self.retrieval_chain.invoke({"input": f"{query}"})
        return response


