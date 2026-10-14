
from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    approved: bool = Field(
        description="Whether the itinerary meets the requirements."
    )
    feedback: str = Field(
        description="Specific problems and suggested corrections."
    )
