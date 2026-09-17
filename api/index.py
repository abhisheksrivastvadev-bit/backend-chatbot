# Import the FastAPI class from the fastapi library to create our API web service
from fastapi import FastAPI
# Import BaseModel from pydantic to define structured data schemas with automatic validation
from pydantic import BaseModel
# from openai import OpenAI
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from portfolio import portfolio_data

load_dotenv()

# Create an instance of the FastAPI application to register routes and middleware
app = FastAPI()

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


# Decorator specifying an HTTP GET route at the root URL path ("/")
@app.get("/api")
# Handler function executed whenever a GET request arrives at "/"
def home():
    # Return a Python dictionary, which FastAPI automatically converts into a JSON response
    return {
        "message": "Chatbot API is running"
    }

def retrieve_portfolio_info(user_message: str):
    print("user_message",user_message)
    user_message = user_message.lower()

    relevant_sections = []

    for section, content in portfolio_data.items():

        keywords = section.lower().split()

        if any(keyword in user_message for keyword in keywords):
            relevant_sections.append(content)

    return "\n".join(relevant_sections)

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

                    You can only answer questions related to Abhishek's portfolio,
                    experience, skills, projects, education, resume, and professional background.

                    If the user asks a question unrelated to Abhishek's portfolio,
                    politely say that you can only answer portfolio-related questions.

                    Do not answer general knowledge questions.
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