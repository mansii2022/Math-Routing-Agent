# backend/scripts/seed_kb.py
from app.agents.retriever import KB

seed = [
  {"question":"Integrate x^2 dx", "answer":"Step 1: ∫x^2 dx = x^3/3 + C"},
  {"question":"Factorize x^3 - 8", "answer":"Step 1: x^3-8=(x-2)(x^2+2x+4)"},
  {"question":"Solve x^2 - 4 = 0", "answer":"Step 1: (x-2)(x+2)=0 ⇒ x=±2"},
  {"question":"Find derivative of x^3+2x", "answer":"Step 1: d/dx(x^3+2x)=3x^2+2"},
  {"question":"Compute probability of 2 heads in 3 tosses", "answer":"Step 1: C(3,2)/2^3=3/8"},
]
KB().add_many(seed)
print("Seeded KB with", len(seed), "items.")
