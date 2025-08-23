from fastapi import APIRouter
from pydantic import BaseModel
from app.graph import build_graph
from ..app.agents.feedback import add_feedback, last_n
from ..app.agents.retriever import KB
import json

router = APIRouter()
graph = build_graph()
kb = KB()

class SolveIn(BaseModel):
    question: str

@router.post("/solve")
def solve(inp: SolveIn):
    state = {"question": inp.question, "contexts": [], "used": "none", "answer": ""}
    out = graph.invoke(state)
    return out

class FeedbackIn(BaseModel):
    question: str
    answer: str
    rating: int
    comment: str | None = None

@router.post("/feedback")
def feedback(inp: FeedbackIn):
    fid = add_feedback(inp.question, inp.answer, inp.rating, inp.comment)
    return {"status": "ok", "id": fid}

@router.get("/feedback/recent")
def feedback_recent():
    rows = last_n(50)
    return {"items": [{"id": r[0], "question": r[1], "rating": r[2], "comment": r[3]} for r in rows]}

class IngestItem(BaseModel):
    question: str
    answer: str

@router.post("/ingest")
def ingest(items: list[IngestItem]):
    kb.ingest([i.dict() for i in items])
    return {"status": "ok", "count": len(items)}
