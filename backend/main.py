from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.router import router

app = FastAPI(title="Agentic Math-RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Include router
app.include_router(router)
