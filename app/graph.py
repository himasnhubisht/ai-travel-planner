
import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from app.state import TravelState
from app.nodes.planner import planner
from app.nodes.transport_researcher import transport_researcher
from app.nodes.researchers import (
    accommodation_researcher,
    activities_researcher,
)
from app.nodes.synthesizer import synthesizer
from app.nodes.evaluator import evaluator
from app.nodes.reviser import reviser
from app.nodes.human_approval import human_approval

from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

MAX_REVISIONS = 2


# Route after automated evaluation.
def route_after_evaluation(state: TravelState) -> str:
    if state["approved"]:
        return "human_approval"

    if state["retry_count"] < MAX_REVISIONS:
        return "reviser"

    return "human_approval"


# Route after human approval or rejection.
def route_after_human(state: TravelState) -> str:
    if state["approved"]:
        return "end"

    if state["retry_count"] < MAX_REVISIONS:
        return "reviser"

    return "end"


# Create the graph.
graph = StateGraph(TravelState)


# Register nodes.
graph.add_node("planner", planner)
graph.add_node("transport_researcher", transport_researcher)
graph.add_node("accommodation_researcher", accommodation_researcher)
graph.add_node("activities_researcher", activities_researcher)
graph.add_node("synthesizer", synthesizer)
graph.add_node("evaluator", evaluator)
graph.add_node("reviser", reviser)
graph.add_node("human_approval", human_approval)


# START -> Planner.
graph.add_edge(START, "planner")


# FAN-OUT: research branches.
graph.add_edge("planner", "transport_researcher")
graph.add_edge("planner", "accommodation_researcher")
graph.add_edge("planner", "activities_researcher")



graph.add_edge(
    [
        "transport_researcher",
        "accommodation_researcher",
        "activities_researcher",
    ],
    "synthesizer",
)


# Synthesize and evaluate.
graph.add_edge("synthesizer", "evaluator")

graph.add_conditional_edges(
    "evaluator",
    route_after_evaluation,
    {
        "reviser": "reviser",
        "human_approval": "human_approval",
    },
)


# Revise and regenerate the itinerary.
graph.add_edge("reviser", "synthesizer")


# Human approval and final routing.
graph.add_conditional_edges(
    "human_approval",
    route_after_human,
    {
        "end": END,
        "reviser": "reviser",
    },
)
conn = sqlite3.connect(
    "travel_checkpoints.sqlite",
    check_same_thread=False,
)

serde = JsonPlusSerializer(
    allowed_msgpack_modules=[
        ("app.schemas.research_plan", "ResearchPlan"),
    ]
)

checkpointer = SqliteSaver(conn, serde=serde)
checkpointer.setup()
app = graph.compile(checkpointer=checkpointer)

