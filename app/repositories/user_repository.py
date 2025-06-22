from sqlmodel import Session, select
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash, verify_password


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """Fetches a user from the database by their ID."""
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> User | None:
    """Fetches a user from the database by their username."""
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def create_user(session: Session, user_create: UserCreate) -> User:
    """Hashes the password and creates a new user in the database."""
    hashed_password = get_password_hash(user_create.password)
    db_user = User(username=user_create.username, hashed_password=hashed_password)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    """Authenticates a user by checking username and password."""
    db_user = get_user_by_username(session, username=username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
