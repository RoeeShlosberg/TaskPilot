from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings


# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Print SQL queries when debug=True
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)


def create_db_and_tables():
    """
    Create database tables from SQLModel definitions
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency to get database session for FastAPI endpoints
    """
    with Session(engine) as session:
        yield session
