from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_db, get_current_user
from ..models.run import Run
from ..models.user import User
from ..schemas.run import RunCreate, RunUpdate, RunResponse

router = APIRouter(prefix="/runs", tags=["runs"])

@router.post("", response_model=RunResponse)
def create_run(
    payload: RunCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    run = Run(
        user_id = current_user.id,
        distance_miles = payload.distance_miles,
        duration_seconds = payload.duration_seconds,
        run_date = payload.run_date
    )

    db.add(run)
    db.commit()
    db.refresh(run)
    return run

@router.get("", response_model=list[RunResponse])
def get_runs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    runs = (
        db.query(Run)
        .filter(Run.user_id == current_user.id)
        .order_by(Run.run_date.desc())
        .all()
    )
    return runs

@router.get("/{run_id}", response_model=RunResponse)
def get_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    run = (
        db.query(Run)
        .filter(Run.id == run_id, Run.user_id == current_user.id)
        .first()
    )

    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return run

@router.put("/{run_id}", response_model=RunResponse)
def update_run(
    run_id: int,
    payload: RunUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    run = (
        db.query(Run)
        .filter(Run.id == run_id, Run.user_id == current_user.id)
        .first()
    )

    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    run.distance_miles = payload.distance_miles
    run.duration_seconds = payload.duration_seconds
    run.run_date = payload.run_date

    db.commit()
    db.refresh(run)

    return run

@router.delete("/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    run = (
        db.query(Run)
        .filter(Run.id == run_id, Run.user_id == current_user.id)
        .first()
    )

    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    db.delete(run)
    db.commit()

    return None