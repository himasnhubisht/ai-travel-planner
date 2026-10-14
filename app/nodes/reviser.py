
from app.state import TravelState


def reviser(state: TravelState) -> dict:
    """Record one revision attempt and reset approval."""

    if state["retry_count"] >= 2:
        raise ValueError("Maximum revision limit reached.")

    return {
        "retry_count": state["retry_count"] + 1,
        "approved": False,
    }
