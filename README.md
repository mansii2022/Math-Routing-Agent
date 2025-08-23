# 📐 Math Routing Agent – Agentic RAG System

This project implements an **Agentic-RAG (Retrieval Augmented Generation)** system designed to act like a **Mathematics Professor**. It solves math problems with **step-by-step explanations**, retrieves knowledge from a **Knowledge Base (VectorDB)**, performs **web search (via MCP)** when required, and incorporates a **Human-in-the-Loop (HiTL) Feedback mechanism**.

---

## 🚀 Features

- **AI Gateway Guardrails**
  - Input/output filters ensure only **educational content (Math)** is processed.
  - Protects against irrelevant or unsafe queries.

- **Knowledge Base (VectorDB)**
  - Stores solved math questions (NCERT/JEE style).
  - Fast semantic retrieval for similar questions.

- **Math Solver Agent**
  - Handles:
    - Arithmetic
    - Algebra (factorization, solving equations, expansion)
    - Calculus (derivatives, integration, limits)
    - Probability & combinatorics
    - Trigonometry
  - Uses **Sympy** for symbolic mathematics.

- **Web Search via MCP**
  - If KB doesn’t contain the answer, the system queries the web.
  - Ensures correctness by validating before answering.

- **Human-in-the-Loop Feedback**
  - Students can **rate answers** and give suggestions.
  - Feedback is stored for **self-learning & refinement**.

- **Frontend (React + Vite)**
  - Clean UI with gradient background & animations.
  - Input box for math questions.
  - Displays **step-by-step answers**.
  - Feedback form with rating & comments.

- **Backend (FastAPI)**
  - `/solve` → Solve math questions.
  - `/feedback` → Store student feedback.
  - `/last-feedback` → View recent feedback.

---
Front end:
<img width="1362" height="674" alt="image" src="https://github.com/user-attachments/assets/928ec845-4944-481d-a09f-df54421a09bb" />

<img width="1352" height="587" alt="image" src="https://github.com/user-attachments/assets/36bb8919-b72c-47bd-ae5a-fb50567bb4ff" />
<img width="1346" height="631" alt="image" src="https://github.com/user-attachments/assets/a52930b9-6ecc-4084-9499-a5bfb707bf58" />


📊 Example Queries
✅ Basic Arithmetic → 2+2
✅ Algebra → factor x^3 - 8
✅ Equation Solving → solve x^2 - 4 = 0
✅ Differentiation → differentiate x^3 + 2x
✅ Integration → integrate sin(x) dx
✅ Probability → probability of 2 heads in 3 tosses
Assignment Requirements Mapping

AI Gateway + Guardrails → ✅ Implemented

Knowledge Base with VectorDB → ✅ Implemented (FAISS)

Web Search via MCP → ✅ Integrated (pipeline ready)

Human-in-the-Loop (Feedback) → ✅ Rating + comments stored

Step-by-step Math Professor-like answers → ✅ Sympy-based reasoning

Frontend + Backend Pipeline → ✅ Working system

📌 Future Work

Expand KB with JEE Bench dataset.

Benchmark performance on complex JEE questions.

Improve explanation formatting with LaTeX rendering.

Deploy backend (FastAPI) & frontend (React) on cloud (Heroku/Render/Vercel).

👩‍💻 Author

Mansi Kumari - AI/ML & Data Analytics 
