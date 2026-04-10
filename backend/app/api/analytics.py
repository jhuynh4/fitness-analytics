from datetime import date, timedelta

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
    seven_days_ago = date.today() - timedelta(days=7)

    #All-time run stats
    total_runs = (
        db.query(func.count(Run.id))
        .filter(Run.user_id == user_id)
        .scalar()
        or 0
    )

    total_miles = (
        db.query(func.sum(Run.distance_miles))
        .filter(Run.user_id == user_id)
        .scalar()
        or 0
    )

    total_duration_seconds = (
        db.query(func.sum(Run.duration_seconds))
        .filter(Run.user_id == user_id)
        .scalar()
        or 0
    )

    avg_pace_seconds_per_mile = (
        round(total_duration_seconds / total_miles, 2)
        if total_miles
        else 0
    )

    #Last 7 days run stats
    runs_last_7_days = (
        db.query(func.count(Run.id))
        .filter(Run.user_id == user_id, Run.run_date >= seven_days_ago)
        .scalar()
        or 0
    )

    miles_last_7_days = (
        db.query(func.sum(Run.distance_miles))
        .filter(Run.user_id == user_id, Run.run_date >= seven_days_ago)
        .scalar()
        or 0
    )

    avg_calories_7d = (
        db.query(func.avg(NutritionLog.calories))
        .filter(NutritionLog.user_id == user_id, NutritionLog.log_date >= seven_days_ago)
        .scalar()
        or 0
    )

    avg_protein_7d = (
        db.query(func.avg(NutritionLog.protein_g))
        .filter(NutritionLog.user_id == user_id, NutritionLog.log_date >= seven_days_ago)
        .scalar()
        or 0
    )

    latest_weight = (
        db.query(WeightLog.weight_lbs)
        .filter(WeightLog.user_id == user_id)
        .order_by(WeightLog.log_date.desc(), WeightLog.id.desc())
        .limit(1)
        .scalar()
    )

    avg_weight_7d = (
        db.query(func.avg(WeightLog.weight_lbs))
        .filter(WeightLog.user_id == user_id, WeightLog.log_date >= seven_days_ago)
        .scalar()
        or 0
    )

    return {
        "total_runs": total_runs,
        "total_miles": round(total_miles, 2) if total_miles else 0,
        "runs_last_7_days": runs_last_7_days,
        "miles_last_7_days": round(miles_last_7_days, 2) if miles_last_7_days else 0,
        "avg_pace_seconds_per_mile": avg_pace_seconds_per_mile,
        "avg_calories_7d": round(avg_calories_7d, 2) if avg_calories_7d else 0,
        "avg_protein_7d": round(avg_protein_7d, 2) if avg_protein_7d else 0,
        "latest_weight": round(latest_weight, 2) if latest_weight else None,
        "avg_weight_7d": round(avg_weight_7d, 2) if avg_weight_7d else 0,
    }

@router.get("/trends")
def get_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.id

    run_rows = (
        db.query(Run.run_date, func.sum(Run.distance_miles))
        .filter(Run.user_id == user_id)
        .group_by(Run.run_date)
        .order_by(Run.run_date.asc())
        .all()
    )

    nutrition_rows = (
        db.query(NutritionLog.log_date, NutritionLog.calories, NutritionLog.protein_g)
        .filter(NutritionLog.user_id == user_id)
        .order_by(NutritionLog.log_date.asc())
        .all()
    )

    weight_rows = (
        db.query(WeightLog.log_date, WeightLog.weight_lbs)
        .filter(WeightLog.user_id == user_id)
        .order_by(WeightLog.log_date.asc())
        .all()
    )

    return {
        "run_miles_by_date": [
            {
                "date": run_date.isoformat(),
                "miles": round(miles, 2) if miles else 0,
            }
            for run_date, miles in run_rows
        ],
        "nutrition_by_date": [
            {
                "date": log_date.isoformat(),
                "calories": calories,
                "protein_g": protein_g,
            }
            for log_date, calories, protein_g in nutrition_rows
        ],
        "weight_by_date": [
            {
                "date": log_date.isoformat(),
                "weight_lbs": round(weight_lbs, 2) if weight_lbs else 0,
            }
            for log_date, weight_lbs in weight_rows
        ],
    }