# AI Backend API 🚀

A scalable backend API built with **Python** and **FastAPI**, powered by **Groq LLMs**, **Gemini Embeddings**, and **Qdrant Vector Database** for high-performance AI retrieval and generation workflows.

This backend supports:
- ⚡ Fast AI inference using Groq
- 🧠 Semantic search with Gemini embeddings
- 📚 Vector storage & retrieval using Qdrant
- 🌐 Web search with Tavily
- 📰 Intelligent web content extraction using Trafilatura & BeautifulSoup
- 🔌 RESTful APIs with FastAPI

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | High-performance API framework |
| Groq LLM | Large Language Model inference |
| Gemini Embeddings | Text embeddings generation |
| Qdrant | Vector database |
| Tavily | Web search API |
| Trafilatura | Web content extraction |
| BeautifulSoup | HTML parsing & scraping |

---

# Features ✨

- AI-powered question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search pipeline
- Web search integration
- Clean article extraction
- Fast and scalable APIs
- Modular architecture

---

# Installation ⚙️

## 1. Clone the Repository

```bash
git clone https://github.com/Intakhab2004/Perplexity-server.git

cd Perplexity-server
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / Mac
```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables 🔐

Create a `.env` file in the root directory:

```env
DB_URI=your_db_uri

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model

GEMINI_API_KEY=your_google_api_key

QDRANT_URL=your_qdrant_url

TAVILY_API_KEY=your_tavily_api_key
```

---

# Running the Server ▶️

```bash
python main.py
```

Server will run at:

```bash
http://127.0.0.1:5000
```

---

# AI Workflow 🧠

```text
User Query
    ↓
Sub-Query Planning
    ↓
Tavily Web Search
    ↓
Trafilatura / BeautifulSoup Parsing
    ↓
Gemini Embeddings
    ↓
Qdrant Vector Search
    ↓
Groq LLM Response Generation
    ↓
Final Answer
```

---

# Future Improvements 📈

- User authentication
- Chat history persistence
- Streaming responses

---

# Contributing 🤝

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a pull request

---

# Author ✨

Built with ❤️ by Intakhab Alam using FastAPI, Groq, Gemini, and Qdrant.
