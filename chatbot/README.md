# Python Chatbot API (FastAPI + Uvicorn)

A lightweight, high-performance RESTful API for a chatbot application built with **FastAPI**, validated with **Pydantic**, and served using **Uvicorn**.

---

## 📖 Table of Contents

- [Core Concepts Explained](#-core-concepts-explained)
  - [What is FastAPI?](#what-is-fastapi)
  - [What is Uvicorn?](#what-is-uvicorn)
  - [How FastAPI and Uvicorn Work Together](#how-fastapi-and-uvicorn-work-together)
- [Project Overview](#-project-overview)
- [Project Directory Structure](#-project-directory-structure)
- [Code Explanation (`main.py`)](#-code-explanation-mainpy)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [API Endpoints & Usage Examples](#-api-endpoints--usage-examples)
  - [1. Health Check / Root Endpoint](#1-health-check--root-endpoint)
  - [2. Chatbot Endpoint](#2-chatbot-endpoint)
- [Interactive API Documentation](#-interactive-api-documentation)

---

## 🧠 Core Concepts Explained

### What is FastAPI?

**[FastAPI](https://fastapi.tiangolo.com/)** is a modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints.

#### Key Features:
- **Fast Performance**: On par with NodeJS and Go (thanks to Starlette and Pydantic under the hood).
- **Automatic Data Validation**: Uses Python type hints and Pydantic models to automatically validate request queries, path parameters, and JSON payloads. If incoming data is invalid, it returns clear HTTP 422 errors automatically.
- **Automatic Interactive Docs**: Generates interactive documentation automatically via OpenAPI specifications (**Swagger UI** at `/docs` and **ReDoc** at `/redoc`).
- **Asynchronous Support**: Native support for Python's `async` and `await`, allowing high concurrency for I/O-bound tasks.
- **Intuitive & Developer-Friendly**: Excellent editor autocomplete, type checks, and reduced code duplication.

---

### What is Uvicorn?

**[Uvicorn](https://www.uvicorn.org/)** is an ultra-fast **ASGI** (Asynchronous Server Gateway Interface) web server implementation for Python.

#### Why do we need a server like Uvicorn?
Python web frameworks (like FastAPI or Starlette) define *how* to handle requests and route them to functions. However, they are not web servers themselves—they cannot directly bind to a network socket or listen for incoming HTTP/WebSocket connections from clients.

Uvicorn acts as the **bridge**:
1. It listens on network ports (e.g., `127.0.0.1:8000`).
2. It receives raw HTTP network requests from clients (browsers, mobile apps, cURL).
3. It converts them into standard ASGI format and hands them over to FastAPI.
4. It takes the response produced by FastAPI and sends it back across the network to the client.

#### WSGI vs. ASGI:
- **WSGI (Web Server Gateway Interface)**: The older Python standard (used by Flask and Django). WSGI is **synchronous**—a worker handles one request from start to finish before moving on to the next.
- **ASGI (Asynchronous Server Gateway Interface)**: The modern standard (used by FastAPI). ASGI allows handling multiple concurrent connections, streaming, WebSockets, and asynchronous long-polling efficiently.

---

### How FastAPI and Uvicorn Work Together

```
   Client (Browser / Postman / cURL)
                  │
          HTTP Request (JSON)
                  ▼
         ┌─────────────────┐
         │     Uvicorn     │  <--- ASGI Web Server (manages network sockets, HTTP protocol)
         └────────┬────────┘
                  │ ASGI Interface
                  ▼
         ┌─────────────────┐
         │     FastAPI     │  <--- Web Framework (handles routing, Pydantic validation)
         └────────┬────────┘
                  │ Calls handler function
                  ▼
              main.py
```

---

## 📁 Project Directory Structure

```text
chatbot/
├── ai_env/       # Python virtual environment (dependencies)
├── main.py       # Main application entry point (FastAPI app and routes)
└── README.md     # Project documentation and guide
```

---

## 🔍 Code Explanation (`main.py`)

Here is how each part of `main.py` works:

```python
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Initialize the FastAPI app instance
app = FastAPI()

# 2. Define the Request Body Schema
# Pydantic validates that the client sends a JSON body with a string "message" field.
class ChatRequest(BaseModel):
    message: str

# 3. Root Endpoint (GET /)
# Useful for health checks to verify that the server is alive.
@app.get("/")
def home():
    return {
        "message": "Chatbot API is running"
    }

# 4. Chat Endpoint (POST /chat)
# Accepts a JSON body validated against ChatRequest and returns the bot's response.
@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message
    return {
        "reply": f"You said: {user_message}"
    }
```

---

## ⚙️ Installation & Setup

### 1. Navigate to the project directory
```bash
cd /Users/admin/Documents/Git/python-chatbot/chatbot
```

### 2. Activate the Virtual Environment
If you already have `ai_env`:
- **macOS / Linux**:
  ```bash
  source ai_env/bin/activate
  ```
- **Windows**:
  ```bash
  ai_env\Scripts\activate
  ```

*(Optional) If creating a new virtual environment from scratch:*
```bash
python3 -m venv ai_env
source ai_env/bin/activate
pip install fastapi uvicorn pydantic
```

---

## 🚀 Running the Application

Start the development server using **Uvicorn**:

```bash
uvicorn main:app --reload
```

### Explanation of the command flags:
- `main`: Refers to the Python file (`main.py`).
- `app`: Refers to the object created inside `main.py` via `app = FastAPI()`.
- `--reload`: Enables auto-reload. The server will restart automatically whenever you edit and save your code.

When started, you should see output similar to:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 📡 API Endpoints & Usage Examples

### 1. Health Check / Root Endpoint

Checks if the API is up and running.

- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/`

#### cURL Example:
```bash
curl -X GET http://127.0.0.1:8000/
```

#### Response:
```json
{
  "message": "Chatbot API is running"
}
```

---

### 2. Chatbot Endpoint

Sends a message to the chatbot and receives a response.

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/chat`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "message": "Hello, how are you?"
  }
  ```

#### cURL Example:
```bash
curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, how are you?"}'
```

#### Response:
```json
{
  "reply": "You said: Hello, how are you?"
}
```

#### Python Example (using `requests`):
```python
import requests

url = "http://127.0.0.1:8000/chat"
payload = {"message": "Tell me a joke"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
# Output: {'reply': 'You said: Tell me a joke'}
```

---

## 📚 Interactive API Documentation

FastAPI automatically generates interactive API documentation. While your server is running, open your browser and navigate to:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - Allows you to test endpoints directly from the browser by clicking **"Try it out"**.
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
  - Clean, organized, publication-ready API documentation.
