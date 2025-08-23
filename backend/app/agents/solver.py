# backend/app/agents/solver.py
from typing import Dict, List
from sympy import symbols, sympify, factor, expand, diff, integrate, Eq, solveset, S
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.sympify import SympifyError

x, y, z = symbols("x y z")

def _eval_arithmetic(q: str):
    # VERY constrained eval using sympy
    try:
        expr = sympify(q.replace("^", "**"))
        val = expr.evalf()
        return float(val)
    except Exception:
        return None

def solve_math(question: str, contexts: List[str] | None = None) -> Dict:
    q = (question or "").strip()
    steps = []

    # 1) Try safe arithmetic quickly
    val = _eval_arithmetic(q)
    if val is not None:
        steps.append(f"Step 1: Evaluate → {val}")
        return {"answer": "\n".join(steps), "used":"solver", "contexts": contexts or []}

    # 2) Pattern commands
    ql = q.lower()
    try:
        if ql.startswith("factorize") or ql.startswith("factor"):
            expr = parse_expr(q.split(" ",1)[1].replace("^","**"))
            res = factor(expr)
            steps += [f"Step 1: Factor the expression", f"Answer: {res}"]
            return {"answer":"\n".join(steps), "used":"solver", "contexts": contexts or []}

        if ql.startswith("expand"):
            expr = parse_expr(q.split(" ",1)[1].replace("^","**"))
            res = expand(expr)
            steps += [f"Step 1: Expand binomial/polynomial", f"Answer: {res}"]
            return {"answer":"\n".join(steps), "used":"solver", "contexts": contexts or []}

        if ql.startswith("solve"):
            expr_str = q.split(" ",1)[1].replace("^","**")
            if "=" in expr_str:
                left,right = expr_str.split("=",1)
                sol = solveset(Eq(parse_expr(left), parse_expr(right)), x, domain=S.Complexes)
            else:
                sol = solveset(parse_expr(expr_str), x, domain=S.Complexes)
            steps += [f"Step 1: Solve equation", f"Answer: {list(sol)}"]
            return {"answer":"\n".join(steps), "used":"solver", "contexts": contexts or []}

        if ql.startswith("differentiate") or ql.startswith("derivative"):
            expr = parse_expr(q.split(" ",1)[1].replace("^","**"))
            res = diff(expr, x)
            steps += [f"Step 1: Differentiate wrt x", f"Answer: {res}"]
            return {"answer":"\n".join(steps), "used":"solver", "contexts": contexts or []}

        if ql.startswith("integrate"):
            expr = parse_expr(ql.replace("integrate","",1).replace("dx","").strip().replace("^","**"))
            res = integrate(expr, x)
            steps += [f"Step 1: Integrate wrt x", f"Answer: {res} + C"]
            return {"answer":"\n".join(steps), "used":"solver", "contexts": contexts or []}

        # Add more JEE patterns as needed...
        return {"answer": f"Could not parse a known math intent for: {question}", "used":"solver", "contexts": contexts or []}

    except SympifyError:
        return {"answer": f"Invalid expression: {question}", "used":"solver", "contexts": contexts or []}
    except Exception as e:
        return {"answer": f"Error: {e}", "used":"solver", "contexts": contexts or []}
