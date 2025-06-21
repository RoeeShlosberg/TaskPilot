import logging
from sqlmodel import Session
from fastapi import HTTPException, status
from app.schemas.user_schema import UserCreate
from app.repositories import user_repository
from app.core.security import create_access_token
from app.models.user_model import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_new_user(session: Session, user_create: UserCreate) -> User:
    """Business logic to register a new user."""
    db_user = user_repository.get_user_by_username(session, username=user_create.username)
    if db_user:
        logger.warning(f"Registration attempt for existing username: {user_create.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    new_user = user_repository.create_user(session, user_create=user_create)
    logger.info(f"New user registered: {new_user.username} (ID: {new_user.id})")
    return new_user

def login_for_access_token(session: Session, form_data) -> dict:
    """Business logic to authenticate user and create access token."""
    user = user_repository.authenticate_user(
        session, username=form_data.username, password=form_data.password
    )
    if not user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}
    )
    logger.info(f"User logged in successfully: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}
