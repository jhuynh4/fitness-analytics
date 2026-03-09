from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fitness_analytics"

#creates connection to PostgreSQL
#create_engine is basically a database connection manager
engine = create_engine(DATABASE_URL)

#session maker creates database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#all database models will inherit from this
Base = declarative_base()