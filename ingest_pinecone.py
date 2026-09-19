import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore


# Load environment variables
load_dotenv()


# -----------------------------------
# 1. Load Resume PDF
# -----------------------------------

loader = PyPDFLoader("Abhishek_Resume.pdf")

documents = loader.load()

print(f"PDF pages loaded: {len(documents)}")


# -----------------------------------
# 2. Split PDF into chunks
# -----------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")


# -----------------------------------
# 3. Create Embedding Model
# -----------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------------
# 4. Get Pinecone index name
# -----------------------------------

index_name = os.getenv("PINECONE_INDEX_NAME")

print(f"Pinecone index: {index_name}")


# -----------------------------------
# 5. Upload documents to Pinecone
# -----------------------------------

vectorstore = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=index_name
)


print("Successfully uploaded resume to Pinecone!")