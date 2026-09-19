






# ########## Pinecone Vector Database for deployment #####################
import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from pinecone import Pinecone

load_dotenv()


# ==============================
# Environment variables
# ==============================

HF_API_KEY = os.getenv("Hugging_Face_Api_Key")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


# ==============================
# Hugging Face client
# ==============================

hf_client = InferenceClient(
    api_key=HF_API_KEY
)


# ==============================
# Pinecone client
# ==============================

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    PINECONE_INDEX_NAME
)


# ==============================
# Generate embedding
# ==============================

def generate_embedding(text: str):

    embedding = hf_client.feature_extraction(
        text,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Hugging Face returns a 1D NumPy array
    # Example:
    # (384,)
    query_vector = embedding.tolist()

    return query_vector


# ==============================
# Retrieve portfolio information
# ==============================

def retrieve_portfolio_info(user_message: str):

    # Step 1:
    # Convert user's question into a vector

    query_vector = generate_embedding(user_message)

    # Step 2:
    # Search Pinecone

    results = index.query(
        vector=query_vector,
        top_k=1,
        include_metadata=True
    )

    # Step 3:
    # Get matching documents

    matches = results.get("matches", [])

    if not matches:
        return ""

    # Step 4:
    # Extract text from metadata

    context = "\n\n".join(
        match["metadata"].get("text", "")
        for match in matches
    )

    return context


# ==============================
# Local test
# ==============================

if __name__ == "__main__":

    query = "What are Abhishek's skills?"

    context = retrieve_portfolio_info(query)

    print("\n========== SEARCH RESULT ==========\n")

    print(context)

# ########## Pinecone Vector Database for deployment #####################






# import os

# from dotenv import load_dotenv

# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_pinecone import PineconeVectorStore


# load_dotenv()


# # -----------------------------------
# # 1. Create embedding model
# # -----------------------------------

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# # -----------------------------------
# # 2. Connect to Pinecone
# # -----------------------------------

# index_name = os.getenv("PINECONE_INDEX_NAME")

# vectorstore = PineconeVectorStore(
#     index_name=index_name,
#     embedding=embeddings
# )


# # -----------------------------------
# # 3. Create retriever
# # -----------------------------------

# retriever = vectorstore.as_retriever(
#     search_kwargs={
#         "k": 1
#     }
# )


# # -----------------------------------
# # 4. Retrieval function
# # -----------------------------------

# def retrieve_portfolio_info(user_message: str):

#     results = retriever.invoke(user_message)

#     context = "\n\n".join(
#         result.page_content
#         for result in results
#     )

#     return context


# # -----------------------------------
# # 5. Test
# # -----------------------------------

# if __name__ == "__main__":

#     query = "What is Abhishek's phone number?"

#     results = retriever.invoke(query)

#     print("\n========== SEARCH RESULTS ==========\n")

#     for i, result in enumerate(results):

#         print(f"----- RESULT {i + 1} -----")

#         print(result.page_content)

#         print("\nMetadata:")

#         print(result.metadata)

#         print()






########## Chroma Vector Database for locally #####################


# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma


# # 1. Load embedding model
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# # 2. Load existing ChromaDB
# vectorstore = Chroma(
#     persist_directory="./chroma_db",
#     embedding_function=embeddings
# )


# # 3. Create retriever
# retriever = vectorstore.as_retriever(
#     search_kwargs={"k": 1}
# )


# # 4. Function used by FastAPI
# def retrieve_portfolio_info(user_message: str):

#     results = retriever.invoke(user_message)

#     context = "\n\n".join(
#         result.page_content
#         for result in results
#     )

#     return context