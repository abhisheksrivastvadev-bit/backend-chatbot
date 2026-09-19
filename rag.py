from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader



# --------------------------------------------------
# 1. Load portfolio document
# --------------------------------------------------

# loader = TextLoader("portfolio.md", encoding="utf-8") # We're telling LangChain to "Read my portfolio.md file."
loader = PyPDFLoader("Abhishek_Resume.pdf")

documents = loader.load() # loads the document into LangChain's document format.

# --------------------------------------------------
# 2. Split document into chunks
# --------------------------------------------------

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


# --------------------------------------------------
# 3. Create embedding model
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 4. Create / load ChromaDB
# --------------------------------------------------

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)


# --------------------------------------------------
# 5. Create retriever
# --------------------------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# --------------------------------------------------
# 6. Retrieval function
# --------------------------------------------------

def retrieve_portfolio_info(user_message: str):

    results = retriever.invoke(user_message)

    context = "\n\n".join(
        result.page_content
        for result in results
    )

    return context

# query = "What is Abhishek Srivastva's mobile number? only give the phone number."
# query = "What is Abhishek Srivastva's CORE TECHNICAL COMPETENCIES."

# results = retriever.invoke(query)

# print("\nRetrieved Documents:\n")

# for result in results:

#     print("--------------------------------------------------")

#     print(result.page_content)
