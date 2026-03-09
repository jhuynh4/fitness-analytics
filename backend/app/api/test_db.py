from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dependencies import get_db

router = APIRouter()

@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"message": "Database session works"}