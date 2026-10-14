
from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    transport_tasks: list[str] = Field(
        description="Research tasks for the transport agent, considering travel dates, "
                    "number of travelers, and the trip budget."
    )

    accommodation_tasks: list[str] = Field(
        description="Research tasks for the accommodation agent, considering "
                    "dates, number of guests, preferences, and budget."
    )

    activities_tasks: list[str] = Field(
        description="Research tasks for the activities agent, considering "
                    "destination, trip duration, interests, and budget."
    )
