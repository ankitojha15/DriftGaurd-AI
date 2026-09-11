from typing import TypedDict
from langgraph.graph import StateGraph, END
from detector import get_columns
from fixer import get_fix
from tester import run_test

class State(TypedDict):
    prod: list
    exp: list
    sql: str
    status: str

def detect(state: State):
    state["prod"] = sorted(get_columns(5433, "prod"))
    state["exp"] = sorted(get_columns(5434, "sandbox"))
    return state

def draft(state: State):
    state["sql"] = get_fix(state["prod"], state["exp"])
    return state

def check(state: State):
    state["status"] = run_test(state["sql"], 5433, "prod")
    return state

g = StateGraph(State)
g.add_node("detect", detect)
g.add_node("draft", draft)
g.add_node("check", check)
g.set_entry_point("detect")
g.add_edge("detect", "draft")
g.add_edge("draft", "check")
g.add_edge("check", END)
app = g.compile()

if __name__ == "__main__":
    print(app.invoke({}))