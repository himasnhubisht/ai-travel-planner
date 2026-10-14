
from langgraph.types import interrupt
from app.state import TravelState


def human_approval(state: TravelState) -> dict:
    decision = interrupt({
        "message": "Review the proposed travel itinerary.",
        "itinerary": state["itinerary"],
        "evaluation_feedback": state["evaluation_feedback"],
        "budget": state["budget"],
    })

    if not isinstance(decision, dict):
        raise ValueError(
            "Approval must be a dictionary with an 'approved' field."
        )

    approved = decision.get("approved")

    if not isinstance(approved, bool):
        raise ValueError("'approved' must be True or False.")

    feedback = decision.get("feedback", "")

    if not isinstance(feedback, str):
        raise ValueError("'feedback' must be a string.")

    return {
        "approved": approved,
        "evaluation_feedback": feedback,
    }
