from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_db, get_current_user
from ..models.user import User
from ..models.weight import WeightLog
from ..schemas.weight import WeightCreate, WeightUpdate, WeightResponse

router = APIRouter(prefix="/weight", tags=["weight"])


@router.post("", response_model=WeightResponse, status_code=status.HTTP_201_CREATED)
def create_weight_log(
    payload: WeightCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    weight_log = WeightLog(
        user_id=current_user.id,
        log_date=payload.log_date,
        weight_lbs=payload.weight_lbs,
    )

    db.add(weight_log)
    db.commit()
    db.refresh(weight_log)

    return weight_log


@router.get("", response_model=list[WeightResponse])
def get_weight_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logs = (
        db.query(WeightLog)
        .filter(WeightLog.user_id == current_user.id)
        .order_by(WeightLog.log_date.desc(), WeightLog.id.desc())
        .all()
    )
    return logs


@router.get("/{weight_id}", response_model=WeightResponse)
def get_weight_log(
    weight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(WeightLog)
        .filter(WeightLog.id == weight_id, WeightLog.user_id == current_user.id)
        .first()
    )

    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")

    return log


@router.put("/{weight_id}", response_model=WeightResponse)
def update_weight_log(
    weight_id: int,
    payload: WeightUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(WeightLog)
        .filter(WeightLog.id == weight_id, WeightLog.user_id == current_user.id)
        .first()
    )

    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")

    log.log_date = payload.log_date
    log.weight_lbs = payload.weight_lbs

    db.commit()
    db.refresh(log)

    return log


@router.delete("/{weight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weight_log(
    weight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(WeightLog)
        .filter(WeightLog.id == weight_id, WeightLog.user_id == current_user.id)
        .first()
    )

    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")

    db.delete(log)
    db.commit()

    return None