import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from pinecone import Pinecone

load_dotenv()

# Hugging Face
hf_client = InferenceClient(
    api_key=os.getenv("Hugging_Face_Api_Key")
)

# Pinecone
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index(
    os.getenv("PINECONE_INDEX_NAME")
)


# Create embedding
query = "What are Abhishek's skills?"

embedding = hf_client.feature_extraction(
    query,
    model="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding type:", type(embedding))
print("Embedding shape/length:", len(embedding))

# Convert to list
query_vector = embedding.tolist()

print("Vector length:", len(query_vector))


# Search Pinecone
result = index.query(
    vector=query_vector,
    top_k=3,
    include_metadata=True
)

print("\n========== PINECONE RESULT ==========\n")
print(result)