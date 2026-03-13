from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_db, get_current_user
from ..models.nutrition import NutritionLog
from ..models.user import User
from ..schemas.nutrition import NutritionCreate, NutritionUpdate, NutritionResponse

router = APIRouter(prefix="/nutrition", tags=["nutrition"])

@router.post("", response_model=NutritionResponse, status_code=status.HTTP_201_CREATED)
def create_nutrition_log(
    payload: NutritionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    nutrition_log = NutritionLog(
        user_id = current_user.id,
        log_date = payload.log_date,
        calories = payload.calories,
        protein_g = payload.protein_g,
        carbs_g = payload.carbs_g,
        fat_g = payload.fat_g,
    )
    
    db.add(nutrition_log)
    db.commit()
    db.refresh(nutrition_log)
    return nutrition_log

@router.get("", response_model=list[NutritionResponse])
def get_nutrition_logs(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    logs = (
        db.query(NutritionLog)
          .filter(NutritionLog.id == current_user.id)
          .order_by(NutritionLog.log_date.desc(), NutritionLog.id.desc())
          .all()
    )
    return logs

@router.get("/{nutrition_id}", response_model=NutritionResponse)
def get_nutrition_log(
    nutrition_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(NutritionLog)
          .filter(NutritionLog.id == nutrition_id, NutritionLog.user_id == current_user.id)
          .first()
    )

    if not log:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    
    return log

@router.put("", response_model=NutritionResponse)
def update_nutrition_log(
    nutrition_id: int,
    payload: NutritionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(NutritionLog)
          .filter(NutritionLog.id == nutrition_id, NutritionLog.user_id == current_user.id)
          .first()
    )

    if not log:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    
    log.log_date = payload.log_date
    log.calories = payload.calories
    log.protein_g = payload.protein_g
    log.carbs_g = payload.carbs_g
    log.fat_g = payload.fat_g

    db.commit()
    db.refresh(log)
    return log

@router.delete("/{nutrition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nutrition_log(
    nutrition_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = (
        db.query(NutritionLog)
          .filter(NutritionLog.id == nutrition_id, NutritionLog.user_id == current_user.id)
          .first()
    )

    if not log:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    
    db.delete(log)
    db.commit()
    return None

