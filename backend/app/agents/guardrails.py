# backend/app/agents/guardrails.py
import re
from typing import Dict

MATH_KEYWORDS = re.compile(
    r"(integrate|differentiate|derivative|limit|probability|permutation|combination|"
    r"matrix|determinant|vector|trigonometry|algebra|calculus|binomial|"
    r"factor|expand|simplify|solve|roots|definite integral|indefinite integral|jee)",
    re.I,
)

def input_guard(user_text: str) -> Dict:
    text = (user_text or "").strip()
    if not text:
        return {"allowed": False, "reason": "Empty question", "cleaned": ""}

    # Only math/education focus
    if not MATH_KEYWORDS.search(text) and not re.search(r"[0-9+\-*/^=()xX]", text):
        return {"allowed": False, "reason": "Non-math content blocked by guardrails", "cleaned": text}

    # Light cleanup
    cleaned = re.sub(r"\s+", " ", text)
    return {"allowed": True, "reason": "ok", "cleaned": cleaned}

def output_guard(answer: str) -> str:
    # Keep it educational + safe
    banned = ["hack", "malware", "violent", "hate"]
    a = (answer or "").strip()
    if any(w in a.lower() for w in banned):
        return "Response redacted by output guardrails."
    # Ensure step-by-step guidance tone
    if not re.search(r"step|⇒|→|\n", a, re.I):
        a = "Step-by-step:\n" + a
    return a
