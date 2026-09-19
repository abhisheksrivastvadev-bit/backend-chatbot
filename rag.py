
########## Pinecone Vector Database for deployment #####################



import os

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()


# -----------------------------------
# 1. Create embedding model
# -----------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------------
# 2. Connect to Pinecone
# -----------------------------------

index_name = os.getenv("PINECONE_INDEX_NAME")

vectorstore = PineconeVectorStore(
    index_name=index_name,
    embedding=embeddings
)


# -----------------------------------
# 3. Create retriever
# -----------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 1
    }
)


# -----------------------------------
# 4. Retrieval function
# -----------------------------------

def retrieve_portfolio_info(user_message: str):

    results = retriever.invoke(user_message)

    context = "\n\n".join(
        result.page_content
        for result in results
    )

    return context


# -----------------------------------
# 5. Test
# -----------------------------------

if __name__ == "__main__":

    query = "What is Abhishek's phone number?"

    results = retriever.invoke(query)

    print("\n========== SEARCH RESULTS ==========\n")

    for i, result in enumerate(results):

        print(f"----- RESULT {i + 1} -----")

        print(result.page_content)

        print("\nMetadata:")

        print(result.metadata)

        print()






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