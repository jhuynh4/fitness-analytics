from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.dependencies import get_db
from ..core.security import create_access_token, verify_password
from ..models.user import User
from ..schemas.user import UserLogin, TokenResponse

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }