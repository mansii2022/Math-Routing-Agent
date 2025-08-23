# Final Proposal (Template)

## 1) Input & Output Guardrails (AI Gateway)
- **Approach**: topic allowlist (math-only), PII redaction, and LLM moderation hook.
- **Why**: keeps scope strictly educational, prevents leakage of private info.

## 2) Knowledge Base
- **Dataset**: GSM8K-style sample (replace with your preferred math dataset like MATH/ProofWiki/JEE).
- **Vector DB**: Qdrant.
- **2–3 test questions**:
  1. If Alice has 3 apples and buys 2 more, how many apples does she have?
  2. A rectangle has length 8 and width 5. What is its area?
  3. Solve for x: 2x + 6 = 18.

## 3) Web Search / MCP Setup
- **Strategy**: Route to web only when KB doesn’t cover; prefer **MCP** tool, else **Tavily → Exa → Serper**.
- **2–3 non-KB questions**:
  - "What is the binomial theorem with a worked example?"
  - "State and prove the AM-GM inequality."
  - "Explain Taylor series expansion for sin(x) up to x^5."

## 4) HiTL (Feedback)
- **Mechanism**: rating + comment stored in SQLite; used for re-ranking and (bonus) DSPy prompt tuning.

## 5) [Bonus] JEE Bench
- Include accuracy from `scripts/run_jeebench.py` and qualitative error analysis.
