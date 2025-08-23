# backend/app/agents/feedback.py
from typing import List, Dict
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///data/feedback.db", echo=False, future=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

def add_feedback(data: Dict):
    with Session() as s:
        fb = Feedback(
            question=data.get("question",""),
            answer=data.get("answer",""),
            rating=int(data.get("rating",0)),
            comment=data.get("comment",""),
        )
        s.add(fb); s.commit()
        return {"ok": True, "id": fb.id}

def last_n(n: int = 5) -> List[Dict]:
    with Session() as s:
        rows = s.query(Feedback).order_by(Feedback.id.desc()).limit(n).all()
        return [
            {"id": r.id, "question": r.question, "answer": r.answer,
             "rating": r.rating, "comment": r.comment, "created_at": r.created_at.isoformat()}
            for r in rows
        ]

# Optional: self-learning hook—good answers can be added to KB
from app.agents.retriever import KB
kb = KB()

def learn_from_feedback(min_rating: int = 4, limit: int = 50):
    with Session() as s:
        rows = (s.query(Feedback)
                  .filter(Feedback.rating >= min_rating)
                  .order_by(Feedback.id.desc())
                  .limit(limit).all())
        qa = []
        for r in rows:
            if r.question and r.answer:
                qa.append({"question": r.question, "answer": r.answer})
        if qa:
            kb.add_many(qa)
    return {"added": len(qa)}
