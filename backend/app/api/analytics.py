from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..core.dependencies import get_db, get_current_user
from ..models.user import User
from ..models.run import Run
from ..models.nutrition import NutritionLog
from ..models.weight import WeightLog

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    # Runs
    total_runs = db.query(func.count(Run.id)).filter(Run.user_id == user_id).scalar() or 0
    total_miles = db.query(func.sum(Run.distance_miles)).filter(Run.user_id == user_id).scalar() or 0

    # Nutrition
    avg_calories = db.query(func.avg(NutritionLog.calories)).filter(NutritionLog.user_id == user_id).scalar() or 0
    avg_protein = db.query(func.avg(NutritionLog.protein_g)).filter(NutritionLog.user_id == user_id).scalar() or 0

    # Weight (latest)
    latest_weight = (
        db.query(WeightLog.weight_lbs)
        .filter(WeightLog.user_id == user_id)
        .order_by(WeightLog.log_date.desc())
        .limit(1)
        .scalar()
    )

    return {
        "total_runs": total_runs,
        "total_miles": round(total_miles, 2) if total_miles else 0,
        "avg_calories": int(avg_calories) if avg_calories else 0,
        "avg_protein": int(avg_protein) if avg_protein else 0,
        "latest_weight": latest_weight,
    }