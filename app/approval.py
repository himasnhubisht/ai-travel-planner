
from langgraph.types import Command

from app.graph import app


def start_trip(initial_state: dict, thread_id: str) -> dict:
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = app.invoke(initial_state, config=config)

    snapshot = app.get_state(config)

    pending_approval = None

    for task in snapshot.tasks:
        for interruption in task.interrupts:
            pending_approval = interruption.value
            break

    return {
        "thread_id": thread_id,
        "status": "waiting_for_approval"
        if pending_approval is not None
        else "completed",
        "approval_request": pending_approval,
        "result": result,
    }


def resume_trip(thread_id: str, decision: dict) -> dict:
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    if not isinstance(decision, dict):
        raise ValueError("Decision must be a dictionary.")

    if not isinstance(decision.get("approved"), bool):
        raise ValueError("'approved' must be True or False.")

    if not isinstance(decision.get("feedback", ""), str):
        raise ValueError("'feedback' must be a string.")

    result = app.invoke(
        Command(resume=decision),
        config=config,
    )

    snapshot = app.get_state(config)

    pending_approval = None

    for task in snapshot.tasks:
        for interruption in task.interrupts:
            pending_approval = interruption.value
            break

    return {
        "thread_id": thread_id,
        "status": "waiting_for_approval"
        if pending_approval is not None
        else "completed",
        "approval_request": pending_approval,
        "result": result,
    }
