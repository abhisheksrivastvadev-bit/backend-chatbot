# Import the FastAPI class from the fastapi library to create our API web service
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import BaseModel from pydantic to define structured data schemas with automatic validation
from pydantic import BaseModel
# from openai import OpenAI
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from portfolio import portfolio_data
from rag import retrieve_portfolio_info

load_dotenv()

# Create an instance of the FastAPI application to register routes and middleware
app = FastAPI()

# Enable CORS for requests from the frontend and external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# client=OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )
hf_token=os.getenv("Hugging_Face_Api_Key")
client=InferenceClient(
    api_key =hf_token
)

# Define a request body schema inheriting from Pydantic's BaseModel
class ChatRequest(BaseModel):
    # Declare an expected input field 'message' that must be of type string
    message: str


# Decorator specifying an HTTP GET route at the root URL path ("/") and ("/api")
@app.get("/")
@app.get("/api")
# Handler function executed whenever a GET request arrives at "/" or "/api"
def home():
    # Return a Python dictionary, which FastAPI automatically converts into a JSON response
    return {
        "message": "Chatbot API is running"
    }

# def retrieve_portfolio_info(user_message: str):
#     print("user_message",user_message)
#     user_message = user_message.lower()

#     relevant_sections = []

#     for section, content in portfolio_data.items():

#         keywords = section.lower().split()

#         if any(keyword in user_message for keyword in keywords):
#             relevant_sections.append(content)

#     return "\n".join(relevant_sections)

# Decorator specifying an HTTP POST route at the path "/chat"
@app.post("/api/chat")
# Handler function that receives and validates the JSON request body using the ChatRequest schema
def chat(request: ChatRequest):

    # Extract the user's message text from the validated request model

    try:
        user_message = request.message

        # response=client.responses.create(
        #     model="gpt-5-mini",
        #     input=user_message
        # )

        relevant_context = retrieve_portfolio_info(user_message)

        response=client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct", 
            # messages=[
            #     {"role": "user", "content": user_message}
            # ]
            messages=[
                    {
                        "role": "system",
                        "content": """
                        You are an AI assistant for Abhishek Srivastva's portfolio website.

                        Answer questions using only the information provided in the portfolio context.

                        Do not invent or assume information that is not present in the context.

                        If the answer cannot be found in the provided context, politely say that the information is not available in Abhishek's portfolio.

                        Only answer questions related to Abhishek's portfolio, experience, skills, projects, education, resume, and professional background.
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Portfolio Information:

                        {relevant_context}

                        User Question:

                        {user_message}
                        """
                    }
                ]
        )
        api_response=response.choices[0].message.content

        # Return a JSON response containing the chatbot's reply
        return {
            "reply": api_response
        }
    except Exception as e:
        return {
            "reply": f"Error: {str(e)}"
        }