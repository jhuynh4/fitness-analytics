from datetime import date, datetime
from pydantic import BaseModel, Field


class WeightCreate(BaseModel):
    log_date: date
    weight_lbs: float = Field(gt=0)


class WeightUpdate(BaseModel):
    log_date: date
    weight_lbs: float = Field(gt=0)


class WeightResponse(BaseModel):
    id: int
    user_id: int
    log_date: date
    weight_lbs: float
    created_at: datetime

    class Config:
        from_attributes = True