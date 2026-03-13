from datetime import date, datetime
from pydantic import BaseModel, Field


class NutritionCreate(BaseModel):
    log_date: date
    calories: int = Field(ge=0)
    protein_g: int = Field(ge=0)
    carbs_g: int = Field(ge=0)
    fat_g: int = Field(ge=0)


class NutritionUpdate(BaseModel):
    log_date: date
    calories: int = Field(ge=0)
    protein_g: int = Field(ge=0)
    carbs_g: int = Field(ge=0)
    fat_g: int = Field(ge=0)


class NutritionResponse(BaseModel):
    id: int
    user_id: int
    log_date: date
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    created_at: datetime

    class Config:
        from_attributes = True