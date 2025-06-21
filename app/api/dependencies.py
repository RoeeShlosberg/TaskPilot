from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.models.user_model import User
from app.schemas.user_schema import TokenData
from app.repositories import user_repository
import logging

# This dependency will look for a token in the Authorization header
# and verify it. The tokenUrl is the endpoint that provides the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

logger = logging.getLogger(__name__)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    """
    Dependency to get the current user from a JWT token.
    Verifies the token, decodes it, and fetches the user from the database.
    Raises HTTPException if the token is invalid or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            logger.warning("Token payload missing username or user ID")
            raise credentials_exception
        token_data = TokenData(username=username, id=user_id)
    except JWTError:
        logger.error("Token validation failed")
        raise credentials_exception
    
    user = user_repository.get_user_by_id(session=db, user_id=token_data.id)
    if user is None:
        logger.warning(f"User not found for ID: {token_data.id}")
        raise credentials_exception
    
    logger.info(f"Current user retrieved: {user.username} (ID: {user.id})")
    return user
