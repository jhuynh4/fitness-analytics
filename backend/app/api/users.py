from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.dependencies import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(
        email=payload.email,
        password_hash = payload.password
    )

    #add object to session
    db.add(user)
    #write to PostgreSQL
    db.commit()
    #refresh row from database so fields like id is populated
    db.refresh(user)

    return user #FastAPI will return as UserResponse model ()

@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users