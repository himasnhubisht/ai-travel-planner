
from typing import TypedDict
from app.schemas.research_plan import ResearchPlan

class TravelState(TypedDict):
    origin: str
    destination: str
    start_date: str
    end_date: str
    budget: float
    travelers: int
    interests: list[str]

    research_plan: dict | None
    transport_info: list[dict]
    accommodation_info: list[dict]
    activities_info: list[dict]

    itinerary: dict
    evaluation_feedback: str
    approved: bool
    retry_count: int
