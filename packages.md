# Project Packages & Dependencies

This document provides a comprehensive breakdown of all Python packages installed in the project's virtual environment (`ai_env`), explaining what each package does, why it is used in this chatbot project, and how it is used in code.

---

## 📋 Quick Summary Table

| Package | Installed Version | Category | Purpose in this Project |
| :--- | :--- | :--- | :--- |
| **`fastapi`** | `0.141.1` | **Core** | Modern web framework for creating API endpoints and documentation |
| **`uvicorn`** | `0.53.0` | **Core** | High-performance ASGI web server to serve FastAPI |
| **`pydantic`** | `2.13.5` | **Core** | Data validation, type enforcement, and request body schemas |
| **`openai`** | `3.14.1` | **Core** | Official OpenAI Python SDK to interact with GPT models |
| **`python-dotenv`** | `1.2.3` | **Core** | Reads `.env` files and loads sensitive secrets into environment variables |
| **`starlette`** | `1.6.0` | Dependency | Low-level ASGI toolkit powering FastAPI routing & HTTP handling |
| **`pydantic_core`** | `2.46.5` | Dependency | High-performance Rust-based core engine for Pydantic v2 |
| **`httpx2`** | `2.13.0` | Dependency | Next-generation async HTTP client used by the OpenAI SDK |
| **`httpcore2`** | `2.13.0` | Dependency | Low-level HTTP engine behind HTTPX |
| **`anyio`** | `4.15.1` | Dependency | Asynchronous concurrency library supporting asyncio and trio |
| **`click`** | `8.5.0` | Dependency | Command Line Interface library used by Uvicorn CLI |
| **`h11`** | `0.16.0` | Dependency | Pure-Python HTTP/1.1 protocol parser used by Uvicorn |
| **`jiter`** | `0.17.0` | Dependency | Ultra-fast JSON parser written in Rust for OpenAI & Pydantic |
| **`idna`** | `3.19` | Dependency | Internationalized Domain Name handling for URL encoding |
| **`sniffio`** | `1.3.1` | Dependency | Detects which async library is running (asyncio vs trio) |
| **`truststore`** | `0.10.4` | Dependency | Verifies SSL/TLS certificates using the OS native certificate store |
| **`typing_extensions`** | `4.16.0` | Dependency | Backports newer Python type hints to earlier Python versions |
| **`typing-inspection`** | `0.4.4` | Dependency | Runtime type introspection helper for Pydantic models |
| **`annotated-types`** | `0.8.0` | Dependency | Reusable type annotations for metadata constraints in Pydantic |
| **`annotated-doc`** | `0.0.5` | Dependency | Generates documentation from annotated type hints |

---

## 🌟 Core / Primary Packages

### 1. `fastapi`
- **Installed Version**: `0.141.1`
- **What it is**: A high-performance Python web framework designed specifically for creating APIs.
- **Why we use it**:
  - Automatically handles HTTP routing (e.g., `GET /`, `POST /chat`).
  - Seamlessly integrates with Pydantic for request body validation.
  - Automatically generates interactive API documentation (Swagger UI at `/docs` and ReDoc at `/redoc`).
- **Example Usage**:
  ```python
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/")
  def home():
      return {"message": "API is online"}
  ```

---

### 2. `uvicorn`
- **Installed Version**: `0.53.0`
- **What it is**: An ASGI (Asynchronous Server Gateway Interface) web server implementation for Python.
- **Why we use it**:
  - FastAPI is an application framework, not a web server. Uvicorn is the server that binds to a network port (e.g., `8000`), receives incoming network requests from browsers/clients, and forwards them into FastAPI.
  - Supports `--reload` for hot reloading during development.
- **Example Usage (Terminal)**:
  ```bash
  uvicorn main:app --reload
  ```

---

### 3. `pydantic`
- **Installed Version**: `2.13.5`
- **What it is**: The most widely used data validation and settings management library for Python.
- **Why we use it**:
  - Defines the expected JSON schema of incoming requests.
  - Automatically validates that incoming requests contain the correct fields and types (e.g., ensuring `message` is a `str`).
  - If a user sends invalid or missing data, Pydantic automatically rejects it with clear HTTP 422 error details.
- **Example Usage**:
  ```python
  from pydantic import BaseModel

  class ChatRequest(BaseModel):
      message: str
  ```

---

### 4. `openai`
- **Installed Version**: `3.14.1`
- **What it is**: The official OpenAI Python client library.
- **Why we use it**:
  - Allows your chatbot application to send prompts to OpenAI's language models (like `gpt-4o`, `gpt-4o-mini`, etc.) and receive AI-generated completions/responses.
  - Handles authentication, streaming, function calling, and token tracking.
- **Example Usage**:
  ```python
  from openai import OpenAI

  client = OpenAI()  # Reads OPENAI_API_KEY from environment automatically

  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Explain gravity in one sentence."}
      ]
  )
  print(response.choices[0].message.content)
  ```

---

### 5. `python-dotenv`
- **Installed Version**: `1.2.3`
- **What it is**: A Python library that reads key-value pairs from a `.env` file and adds them to environment variables (`os.environ`).
- **Why we use it**:
  - Protects secret credentials like your `OPENAI_API_KEY` by keeping them in a local `.env` file rather than hardcoding them into source code.
  - Prevents accidental leaks of secret API keys to public Git repositories.
- **Example Usage**:
  ```python
  import os
  from dotenv import load_dotenv

  # Loads variables from .env into the environment
  load_dotenv()

  api_key = os.getenv("OPENAI_API_KEY")
  ```

---

## ⚙️ Underlying Dependencies & Utilities

These packages were installed automatically as dependencies of the core packages above:

### Web & Concurrency Stack
- **`starlette` (`1.6.0`)**: The foundational ASGI toolkit that FastAPI is built directly on top of. Starlette handles requests, responses, status codes, and routing internals.
- **`anyio` (`4.15.1`)**: A modern asynchronous networking and concurrency library that provides a common API for both Python's built-in `asyncio` and `trio`.
- **`h11` (`0.16.0`)**: A pure-Python implementation of the HTTP/1.1 protocol state machine used by Uvicorn to parse incoming HTTP requests.
- **`sniffio` (`1.3.1`)**: A lightweight utility library that allows code to detect whether it is executing inside `asyncio` or `trio`.

### HTTP & Networking Stack (used by OpenAI SDK)
- **`httpx2` (`2.13.0`) & `httpcore2` (`2.13.0`)**: Next-generation HTTP client libraries providing both sync and async HTTP request capabilities, connection pooling, and HTTP/2 support for OpenAI API calls.
- **`idna` (`3.19`)**: Implements Internationalized Domain Names in Applications (RFC 5891) for handling non-ASCII domain characters.
- **`truststore` (`0.10.4`)**: Connects Python's `ssl` module to the native system certificate store (macOS Keychain, Windows Cert Store) for robust HTTPS verification.

### Data & Validation Internals
- **`pydantic_core` (`2.46.5`)**: The core validation engine for Pydantic v2, written in Rust for lightning-fast parsing and serialization.
- **`jiter` (`0.17.0`)**: An ultra-fast JSON parser written in Rust, utilized by the OpenAI SDK and Pydantic for parsing API payloads.
- **`annotated-types` (`0.8.0`)**: Provides metadata annotations (like `Gt`, `Lt`, `MinLen`) used with `typing.Annotated` in Pydantic.
- **`annotated-doc` (`0.0.5`)**: Extracts documentation strings from annotated types.
- **`typing_extensions` (`4.16.0`)**: Enables modern type hinting features in Python versions that do not yet include them natively.
- **`typing-inspection` (`0.4.4`)**: Inspection tools for analyzing Python type hints at runtime.

### CLI & Tools
- **`click` (`8.5.0`)**: A composable command line interface toolkit used by Uvicorn to power its CLI command `uvicorn main:app --reload`.
- **`pip` (`24.0`)** & **`setuptools` (`65.5.0`)**: Standard Python package installer and build utilities.

---

## 💡 How to Recreate or Export Dependencies

### 1. Export current dependencies to `requirements.txt`:
```bash
pip freeze > requirements.txt
```

### 2. Install all dependencies on a new machine:
```bash
pip install -r requirements.txt
```
