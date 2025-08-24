
# 📐 Math Routing Agent – Agentic RAG System

This project implements an **Agentic-RAG architecture** that replicates a mathematical professor. The system is capable of solving mathematics problems step by step, simplifying the solution for students.

---

## 🚀 Features

### ✅ AI Gateway Guardrails

* Ensures the system only handles **mathematics-related content**.
* Input/Output guardrails prevent hallucinations and irrelevant answers.

### ✅ Knowledge Base Creation (RAG)

* Uses a **VectorDB-based Knowledge Base** to store and retrieve solved math problems.
* If a user’s question exists in the KB, the system fetches and provides a **step-by-step solution**.
* Knowledge base is seeded via `seed_kb.py`.

### ✅ Web Search / MCP Integration

* If the solution is **not found in the KB**, the pipeline is designed to route through **Web Search / MCP**.
* MCP hooks are added to enable future integration with external sources.
* If no reliable answer is found, the system avoids giving incorrect results.

### ✅ Human-in-the-Loop (HiTL) Feedback

* Feedback mechanism integrated in both **backend** and **frontend**.
* Users can submit a **rating + comment** after receiving an answer.
* Feedback is processed and stored in-memory (future work: persistent DB storage).

### ✅ Step-by-Step Explanations

* The solver explains solutions like a **math professor**:

  * Algebra (factorization, expansion, equations)
  * Calculus (integration, differentiation)
  * Probability & Statistics
  * Arithmetic & JEE-level questions

### ⚡ Bonus (Partial)

* Hooks available for **JEE Benchmarking dataset** (future improvement).
* MCP and DSPy integration pathways included in design.

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python), SymPy (math solving), FAISS (VectorDB)
* **Frontend:** React + Vite
* **Database:** VectorDB for KB, in-memory feedback (future: SQLite/Postgres)

---

## 📂 Project Structure

```
math-routing-agent/
│── backend/
│   ├── app/
│   │   ├── agents/        # solver, retriever, feedback
│   │   ├── routes/        # API routes
│   │   ├── scripts/       # KB seeding
│   │   ├── graph.py       # RAG pipeline
│   │   └── main.py        # FastAPI entrypoint
│── frontend/
│   ├── src/               # React frontend
│   └── package.json
│── data/                  # Knowledge base / vector store
│── docs/                  # Documentation
│── README.md              # This file
```

---

## ▶️ How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/<your-username>/math-routing-agent.git
cd math-routing-agent
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

# Seed the knowledge base
python -m app.scripts.seed_kb

# Start server
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit: **[http://localhost:5173](http://localhost:5173)**

---

## 🖼️ Screenshots

* **Frontend UI**
  <img width="1359" height="601" alt="image" src="https://github.com/user-attachments/assets/1aea7ed0-1d08-490d-91f1-45600a981180" />
  <img width="1365" height="600" alt="image" src="https://github.com/user-attachments/assets/93f61280-f523-4eba-bc13-5bc88a0867ba" />



* **Postman Test**
  <img width="1355" height="675" alt="image" src="https://github.com/user-attachments/assets/30672741-e629-4523-925c-752d39fbf5bb" />
  <img width="1360" height="719" alt="image" src="https://github.com/user-attachments/assets/d3b14187-bfec-4ebc-a85e-dba69735b1f4" />
---

## 📊 Future Improvements

* Persistent storage for feedback (SQLite/Postgres).
* Fully integrated **Web Search + MCP pipeline**.
* Benchmarking on **JEE dataset**.

---

## 📌 Summary

This project **meets the assignment requirements**:

* Agentic RAG with KB + Web Search fallback.
* Guardrails for education-focused math solving.
* Human-in-the-loop feedback.
* Step-by-step professor-like explanations.

---

✨ Developed by **Mansi Kumari**

---

