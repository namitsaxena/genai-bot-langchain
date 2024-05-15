from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter
import os

# sentence transformer model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

v_input_file = os.getenv("INPUT_FILE")
if v_input_file is None:
    v_input_file = "./state_of_the_union.txt"

v_chunk_size = os.getenv("CHUNK_SIZE")
if v_chunk_size is None:
    v_chunk_size = 1000
else:
    v_chunk_size = int(v_chunk_size)

v_query = os.getenv("QUERY")
if v_query is None:
    v_query = "What did the president say about Ketanji Brown Jackson"

print(f"Running with input file: {v_input_file}, Chunk Size: {v_chunk_size}, Query: {v_query}")

print("Loading Document...")
# load the document and split it into chunks
loader = TextLoader(v_input_file)
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=v_chunk_size, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)

# query it
query = v_query
docs = db.similarity_search(query)

# print results
print(docs[0].page_content)
