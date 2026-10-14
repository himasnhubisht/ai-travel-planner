
from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator


class TripRequest(BaseModel):
    origin: str = Field(min_length=2, max_length=150)
    destination: str = Field(min_length=2, max_length=150)

    start_date: date
    end_date: date

    budget: float = Field(gt=0, le=100_000_000)
    travelers: int = Field(ge=1, le=50)

    interests: list[str] = Field(min_length=1, max_length=20)

    @field_validator("origin", "destination")
    @classmethod
    def validate_location(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Location cannot be blank.")

        return value

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, values: list[str]) -> list[str]:
        cleaned = [interest.strip() for interest in values]

        if any(not interest for interest in cleaned):
            raise ValueError("Interests cannot contain blank values.")

        # Remove duplicates without changing their order.
        return list(dict.fromkeys(cleaned))

    @model_validator(mode="after")
    def validate_trip(self):
        if self.origin.casefold() == self.destination.casefold():
            raise ValueError("Origin and destination must differ.")

        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date.")

        if self.start_date < date.today():
            raise ValueError("Start date cannot be in the past.")

        return self



class ApprovalRequest(BaseModel):
    approved: bool
    feedback: str = Field(default="", max_length=2000)
