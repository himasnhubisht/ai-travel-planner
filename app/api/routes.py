
from uuid import uuid4

from fastapi import APIRouter

from app.api.schemas import TripRequest
from app.approval import start_trip

from app.api.schemas import ApprovalRequest, TripRequest
from app.approval import start_trip, resume_trip

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Travel Planner API is running"
    }


@router.get("/")
def root():
    return {
        "message": "AI Travel Planner API is running",
        "docs": "/docs",
        "health": "/health"
    }


@router.post("/trips")
def create_trip(request: TripRequest):
    thread_id = str(uuid4())

    initial_state = {
        "origin": request.origin,
        "destination": request.destination,
        "start_date": request.start_date.isoformat(),
        "end_date": request.end_date.isoformat(),
        "budget": request.budget,
        "travelers": request.travelers,
        "interests": request.interests,
        "research_plan": None,
        "transport_info": [],
        "accommodation_info": [],
        "activities_info": [],
        "itinerary": {},
        "evaluation_feedback": "",
        "approved": False,
        "retry_count": 0,
    }

    result = start_trip(initial_state, thread_id)

    return {
        "thread_id": result["thread_id"],
        "status": result["status"],
        "approval_request": result["approval_request"],
    }



@router.post("/trips/{thread_id}/approval")
def approve_trip(thread_id: str, decision: ApprovalRequest):
    workflow = resume_trip(
        thread_id=thread_id,
        decision=decision.model_dump()
    )

    state = workflow.get("result", {})
    itinerary = state.get("itinerary", {})

    return {
        "thread_id": workflow["thread_id"],
        "status": workflow["status"],
        "approved": state.get("approved", False),
        "itinerary": itinerary.get("content", ""),
        "evaluation_feedback": state.get("evaluation_feedback", ""),
    }
