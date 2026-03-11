from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy import func
from ..core.database import Base
class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    distance_miles = Column(Float, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    run_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())