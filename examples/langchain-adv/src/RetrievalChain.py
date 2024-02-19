
class RetrievalChain:
    """
    https://python.langchain.com/docs/get_started/quickstart
    """
    def __init__(self):
        self.loader = None
        self.embeddings = None
        self.vector = None
        self.document_chain = None
        self.retrieval_chain = None

    def setup_loader(self, url="https://docs.smith.langchain.com"):
        from langchain_community.document_loaders import WebBaseLoader
        self.loader = WebBaseLoader(url)

    def setup_embedding(self, model="textembedding-gecko@001"):
        from langchain_google_vertexai import VertexAIEmbeddings
        self.embeddings = VertexAIEmbeddings(model_name=model)

    def load_data(self):
        docs = self.loader.load()
        return docs

    # https://python.langchain.com/docs/integrations/text_embedding/google_vertex_ai_palm
    # https://python.langchain.com/docs/modules/data_connection/text_embedding/
    def get_embedding(self, text="This is a text document"):
        # takes a single text
        query_result = self.embeddings.embed_query(text)
        # print(f"Query Result: {query_result[0:5]}")

        # takes as input multiple texts
        doc_result = self.embeddings.embed_documents([text])
        # print(f"Document Result: {doc_result[0:5]}")
        return query_result

    def load_vector_db(self, docs):
        """

        :param docs: documents from loader (web, etc)
        :param embeddings: embeddings model (not embedding for a text)
        :return:
        """
        from langchain_community.vectorstores import FAISS
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        self.vector = FAISS.from_documents(documents, self.embeddings)

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

    def query_static_context(self):
        """
        test method with static query and context
        :return:
        """
        from langchain_core.documents import Document

        return self.document_chain.invoke({
            "input": "how can langsmith help with testing?",
            "context": [Document(page_content="langsmith can let you visualize test results")]
        })

    def query_with_retrieval(self, query):
        response = self.retrieval_chain.invoke({"input": f"{query}"})
        # print(response["answer"])
        # LangSmith offers several features that can help with testing:...
        return response


