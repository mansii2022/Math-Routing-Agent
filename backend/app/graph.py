# backend/app/graph.py
from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph, START, END
from app.agents.guardrails import input_guard, output_guard
from app.agents.retriever import KB
from app.agents.search_mcp import smart_search
from app.agents.solver import solve_math

kb = KB()

class State(TypedDict, total=False):
    question: str
    contexts: List[str]
    used: Literal["kb","web","solver","none"]
    answer: str

def node_guard_in(state: State) -> State:
    g = input_guard(state["question"])
    if not g["allowed"]:
        return {**state, "used":"none", "contexts":[], "answer": f"Sorry, only math questions. ({g['reason']})"}
    return {**state, "question": g["cleaned"]}

def node_kb(state: State) -> State:
    if state.get("answer"): return state
    res = kb.retrieve(state["question"], k=3)
    if res["hit"]:
        # Use top KB item as context; still run solver to keep step-by-step
        ctx = [f"Q: {r['question']} | A: {r['answer']}" for r in res["results"]]
        sol = solve_math(state["question"], contexts=ctx)
        return {**state, "used":"kb", "contexts": ctx, "answer": sol["answer"]}
    return {**state, "used":"none", "contexts":[]}

def node_web(state: State) -> State:
    if state.get("answer"): return state
    sr = smart_search(state["question"])
    ctx = sr["snippets"] if sr["ok"] else []
    if not ctx:
        return state
    sol = solve_math(state["question"], contexts=ctx)
    return {**state, "used":"web", "contexts": ctx, "answer": sol["answer"]}

def node_solver(state: State) -> State:
    if state.get("answer"): return state
    sol = solve_math(state["question"], contexts=[])
    return {**state, "used":"solver", "contexts": [], "answer": sol["answer"]}

def node_guard_out(state: State) -> State:
    return {**state, "answer": output_guard(state.get("answer",""))}

def build_graph():
    g = StateGraph(State)
    g.add_node("guard_in", node_guard_in)
    g.add_node("kb", node_kb)
    g.add_node("web", node_web)
    g.add_node("solver", node_solver)
    g.add_node("guard_out", node_guard_out)

    g.add_edge(START, "guard_in")
    g.add_edge("guard_in", "kb")
    g.add_edge("kb", "web")
    g.add_edge("web", "solver")
    g.add_edge("solver", "guard_out")
    g.add_edge("guard_out", END)
    return g.compile()
