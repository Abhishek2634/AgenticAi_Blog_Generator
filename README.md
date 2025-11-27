# ✍️ AI Blog Generator

A production-ready AI application that generates SEO-optimized blog posts in multiple languages (English, Hindi, French) using LangGraph agents and Groq's LLaMA 3 models.

This project features a decoupled architecture with a FastAPI backend for agentic workflow orchestration and a Streamlit frontend for user interaction.

---

## 🚀 Features

- Multi-Language Support: Generate content in English, Hindi, or French.
- Agentic Workflow: Uses LangGraph to orchestrate stateful AI agents.
- High-Performance LLM: Powered by Groq (LLaMA 3) for ultra-fast inference.
- Decoupled Architecture:
  - Backend: FastAPI service running LangGraph workflows.
  - Frontend: Streamlit UI for easy topic input and markdown rendering.
- Dockerized: Fully containerized deployment for platforms like Hugging Face Spaces.

---

## 🛠️ Tech Stack

- Orchestration: LangGraph & LangChain
- LLM Inference: Groq API (LLaMA 3)
- Backend: FastAPI, Uvicorn
- Frontend: Streamlit
- Language: Python 3.9+

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Abhishek2634/AgenticAi_Blog_Generator.git
cd AgenticAi_Blog_Generator
```

### 2. Environment Variables
Create a `.env` file in the root directory with at least:

```
GROQ_API_KEY=gsk_...
BACKEND_URL="http://localhost:8000"
LANGCHAIN_API_KEY=lsv2_...          # Optional, for tracing
LANGCHAIN_TRACING_V2=true
```

### 3. Run Locally (Docker)
```bash
docker build -t blog-generator .
docker run -p 7860:7860 --env-file .env blog-generator
```

### 4. Run Locally (Manual)

Backend:
```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Frontend (in a separate terminal):
```bash
    streamlit run streamlit_app.py
```

---

## 🔌 API Documentation

Once running, access the Swagger UI at `/docs` on the backend server (e.g., http://localhost:8000/docs).

- POST `/blogs`: Triggers the blog generation workflow.  
  - Payload example:
  ```json
  {
    "topic": "Machine Learning",
    "language": "hindi"
  }
  ```

---

## ☁️ Deployment

This project is designed to be deployed on Hugging Face Spaces using the Docker SDK.

1. Create a new Space with the **Docker** SDK.
2. Upload the repository files (or push via Git).
3. Add `GROQ_API_KEY` in the Space Settings → Variables and secrets.
4. The provided `Dockerfile` should start the FastAPI backend on port `7860` by default.

---

## Security & Notes

- Keep your API keys secret. Use environment variables or the platform's secret manager.
- Groq LLaMA 3 usage may incur costs; monitor usage and quotas.
- If you enable LangChain tracing or other telemetry, confirm whether you want to store traces externally.

---

## Contributing

Contributions, issues, and feature requests are welcome. For larger changes, please open a PR with a clear description and tests/examples where relevant.

---

## License & Contact

Include your preferred license and contact information here (e.g., MIT License, email, or GitHub handle).

---

Built with ❤️ using LangGraph & Groq