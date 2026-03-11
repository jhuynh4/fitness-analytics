from datetime import date, datetime
from pydantic import BaseModel, Field


class RunCreate(BaseModel):
    distance_miles: float = Field(gt=0)
    duration_seconds: int = Field(gt=0)
    run_date: date

class RunUpdate(BaseModel):
    distance_miles: float = Field(gt=0)
    duration_seconds: int = Field(gt=0)
    run_date: date

class RunResponse(BaseModel):
    id: int
    user_id: int
    distance_miles: float
    duration_seconds: int
    run_date: date
    created_at: datetime

    class Config:
        from_attributes = True