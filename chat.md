## 🚀 "I have started building an AI-powered chatbot for my portfolio website using React.js and Python FastAPI.
* The frontend is built with React.js, and I created a Python FastAPI backend that acts as an API layer between the frontend and the LLM.
* Initially, I connected the backend with Hugging Face's Inference API and integrated the meta-llama/Llama-3.1-8B-Instruct model.
* I created a /chat POST endpoint using FastAPI. The endpoint accepts the user's message as a JSON request, validates it using Pydantic, sends the request to the Llama model, and returns the generated response back to the frontend.
* Then I customized the chatbot specifically for my portfolio. Instead of allowing it to behave like a general-purpose chatbot, I added a system prompt that instructs the model to answer only questions related to my professional experience, skills, projects, resume, and background.

* I also created a portfolio_context containing my professional information and pass that context along with the user's question to the LLM. This allows the model to generate answers based on my portfolio information.

So currently, the flow is:

## React.js → FastAPI → Portfolio Context + System Prompt → Llama 3.1 → FastAPI → React.js.

- **At this stage**, the portfolio information is hardcoded as context. My next step is to implement RAG (Retrieval-Augmented Generation) so that instead of sending the entire portfolio to the LLM for every question, I can retrieve only the relevant information from my portfolio and provide that as context to the model.

- After that, I plan to explore embeddings, a vector database, retrieval, and eventually LangChain to make the chatbot more scalable and reliable."

**If interviewer asks: "Why did you use a system prompt?"**

You can say:

"The system prompt defines the behavior and role of the LLM. I use it to tell the model that it is a portfolio assistant and should only answer questions related to my professional information rather than general knowledge questions."

**If they ask: "What is portfolio_context?"**

Say:

"portfolio_context is the knowledge that I'm currently providing to the LLM about myself. It contains information such as my experience, skills, and projects. I'm injecting that context into the prompt along with the user's question so the LLM can generate a relevant response."

**If they ask: "Why RAG if you already have portfolio_context?"**

You can answer:

"Currently, I'm passing the portfolio information directly as context, which works for a small amount of data. But as the portfolio grows with more projects, experience, documents, and other information, sending the entire context for every question becomes inefficient. With RAG, I can retrieve only the relevant information based on the user's query and send that smaller context to the LLM. This improves scalability and helps keep the responses grounded in my actual portfolio data."

**If they ask: "What happens when someone asks 'What is Python?'"**

You can say:

"I've instructed the LLM through the system prompt to answer only portfolio-related questions. Since the chatbot is intended to represent my portfolio rather than act as a general-purpose assistant, unrelated questions should be rejected or politely declined. However, I also understand that a prompt alone isn't a hard security boundary, so my next step is to add application-level filtering and RAG-based retrieval to make this behavior more reliable."

That last sentence is particularly useful because it shows you understand the limitation of prompt-only control, rather than simply saying "the prompt prevents it."

🧠 **The 30-second version**

"I built a portfolio AI assistant using React.js, FastAPI, Hugging Face, and Llama 3.1 8B. React.js handles the chat UI, while FastAPI exposes a /chat endpoint and communicates with the LLM through Hugging Face. I added a system prompt to define the assistant's role and provided my portfolio information as context so the model can answer questions about my experience, skills, and projects. Currently the portfolio context is hardcoded, and my next step is to implement RAG with embeddings and a vector database so the system can dynamically retrieve relevant portfolio information instead of passing the entire portfolio to the LLM."


### 🧠 Learning Roadmap

✅ FastAPI
      ↓
✅ Hugging Face + Llama
      ↓
✅ System Prompt
      ↓
✅ Portfolio Context
      ↓
👉 Simple Retrieval
      ↓
👉 Embeddings
      ↓
👉 Vector Database
      ↓
👉 Semantic Search
      ↓
👉 RAG
      ↓
👉 Conversation Memory
      ↓
👉 LangChain
      ↓
React.js integration
      ↓
Production improvements