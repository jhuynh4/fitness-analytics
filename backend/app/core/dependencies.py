from .database import SessionLocal

def get_db():
    #creates database session
    db = SessionLocal()
    try:
        #gives session to the route
        yield db
    finally:
        #closes the session once request finishes
        db.close()