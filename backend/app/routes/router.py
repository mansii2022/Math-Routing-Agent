from fastapi import APIRouter
from pydantic import BaseModel
from app.graph import build_graph
from app.agents.feedback import add_feedback, last_n, learn_from_feedback

router = APIRouter()
graph = build_graph()  # CompiledStateGraph

class QuestionRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int
    comment: str = ""

@router.post("/solve")
def solve(req: QuestionRequest):
    out = graph.invoke({"question": req.question})
    return {"answer": out.get("answer",""), "used": out.get("used","none"), "contexts": out.get("contexts",[])}

@router.post("/feedback")
def feedback(req: FeedbackRequest):
    return add_feedback(req.dict())

@router.get("/last-feedback")
def get_last(n: int = 5):
    return last_n(n)

@router.post("/admin/learn")
def learn(min_rating: int = 4, limit: int = 50):
    return learn_from_feedback(min_rating, limit)
