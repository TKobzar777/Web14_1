from enum import Enum

from pydantic import BaseModel, EmailStr
from typing import Optional

class RoleEnum(str, Enum):
    """
    Enum representing the roles available in the system.

    Attributes:
        USER (str): The 'user' role.
        ADMIN (str): The 'admin' role.
    """
    USER = "user"
    ADMIN = "admin"

class RoleBase(BaseModel):
    """
    Base model for role information.

    Attributes:
        id (int): The unique identifier for the role.
        name (RoleEnum): The name of the role.
    """
    id: int
    name: RoleEnum

class UserBase(BaseModel):
    """
    Base model for user information.

    Attributes:
        email (EmailStr): The email address of the user.
    """
    email: EmailStr

class UserCreate(UserBase):
    """
    Model for creating a new user.

    Attributes:
        password (str): The password for the new user.
    """
    password: str

class UserResponse(UserBase):
    """
    Model for the response when retrieving a user.

    Attributes:
        id (int): The unique identifier for the user.
        is_active (bool): Indicates whether the user is active.
        role (RoleBase | None): The role of the user (optional).
    """
    id: int
    is_active: bool
    role: RoleBase | None

    class Config:
        """
        Configuration for the Pydantic model.

        Attributes:
            from_attributes (bool): Whether to use attributes from the model's class.
        """
        from_attributes = True

class Token(BaseModel):
    """
    Model for the token information.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The type of the token.
    """
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Model for the token data.

    Attributes:
        email (Optional[str]): The email address associated with the token (optional).
    """
    email: Optional[str] = None