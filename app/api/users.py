from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
import logging

from app.db.session import get_session
from app.schemas.user_schema import UserCreate, UserPublic, Token
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_session)):
    """Register a new user."""
    try:
        new_user = user_service.register_new_user(session=db, user_create=user_in)
        logger.info(f"User registered successfully: {new_user.username} (ID: {new_user.id})")
        return new_user
    except HTTPException as e:
        # Re-raise HTTPException from the service layer
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration.",
        )


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """Authenticate user and return a JWT access token."""
    try:
        token_data =  user_service.login_for_access_token(session=db, form_data=form_data)
        logger.info(f"Created access token for user: {form_data.username}")
        return token_data
    except HTTPException as e:
        # Re-raise HTTPException from the service layer (e.g., 401 Unauthorized)
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login.",
        )
