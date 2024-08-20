from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db import get_db
from src.auth.models import User
from src.auth.repo import UserRepository

from src.auth.schemas import TokenData, RoleEnum
from config.general import settings


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
VERIFICATION_TOKEN_EXPIRE_HOURS = 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_verification_token(email: str) -> str:
    """
    Create a JWT verification token for the given email address.

    Args:
        email (str): The email address to include in the token.

    Returns:
        str: The encoded JWT verification token.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        hours=VERIFICATION_TOKEN_EXPIRE_HOURS
    )
    to_encode = {"exp": expire, "sub": email}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_verification_token(token: str) -> str | None:
    """
    Decode a JWT verification token and return the email address.

    Args:
        token (str): The JWT verification token to decode.

    Returns:
        str | None: The email address if the token is valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token for the given data.

    Args:
        data (dict): The data to include in the token.
        expires_delta (timedelta | None): The expiration time delta for the token.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT refresh token for the given data.

    Args:
        data (dict): The data to include in the token.
        expires_delta (timedelta | None): The expiration time delta for the token.

    Returns:
        str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData | None:
    """
    Decode a JWT access token and return the token data.

    Args:
        token (str): The JWT access token to decode.

    Returns:
        TokenData | None: The token data if the token is valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return TokenData(email=email)
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Get the current user based on the provided JWT token.

    Args:
        token (str): The JWT token to decode and validate.
        db (AsyncSession): The asynchronous database session.

    Returns:
        User: The current user if the token is valid.

    Raises:
        HTTPException: 401 if the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exception
    user_repo = UserRepository(db)
    user = await user_repo.get_user(token_data.email)
    if user is None:
        raise credentials_exception
    return user

class RoleChecker:
    """
    Dependency to check if the current user has one of the allowed roles.

    Attributes:
        allowed_roles (list[RoleEnum]): The list of allowed roles.
    """
    def __init__(self, allowed_roles: list[RoleEnum]):
        self.allowed_roles = allowed_roles

    async def __call__(self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
        """
        Check if the current user has one of the allowed roles.

        Args:
            token (str): The JWT token to decode and validate.
            db (AsyncSession): The asynchronous database session.

        Returns:
            User: The current user if they have one of the allowed roles.

        Raises:
            HTTPException: 403 if the user does not have one of the allowed roles.
        """
        user = await get_current_user(token, db)
        if user.role.name not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return user
