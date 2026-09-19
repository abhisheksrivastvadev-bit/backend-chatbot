from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# loader = TextLoader("portfolio.md", encoding="utf-8") # We're telling LangChain to "Read my portfolio.md file."
loader = PyPDFLoader("Abhishek_Resume.pdf")

documents = loader.load() # loads the document into LangChain's document format.

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
# # Splitting the document into smaller chunks so that embeddings can be created.
# '''Why?

# Imagine your portfolio contains 10,000 words.

# We don't want one giant document.

# We divide it into smaller chunks.

# chunks = text_splitter.split_documents(documents)

# For example:

# portfolio.md

#         ↓

# Chunk 1
# Professional Summary

# Chunk 2
# Frontend Skills

# Chunk 3
# Backend Skills

# Chunk 4
# AgentIQ

# Chunk 5
# Tradyon

# Chunk 6
# Exhibition Gear
# ...

# '''

chunks = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("ChromaDB created successfully.")