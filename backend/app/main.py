from fastapi import FastAPI
from .core.database import Base, engine
from .models import user
from .api.test_db import router as test_db_router
from .api.users import router as users_router
from .api.auth import router as auth_router
from .api.me import router as me_router

app = FastAPI(title="Fitness Analytics API")

#create all tables that inherit from Base
Base.metadata.create_all(bind=engine)

app.include_router(test_db_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(me_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}