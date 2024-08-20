from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base


class Role(Base):
    """
    SQLAlchemy model representing a role of users in the database.

    Attributes:
        id (int): The primary key of the role.
        name (str): The name of the role, which is unique.
    """
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)

class User(Base):
    """
    SQLAlchemy model representing a user in the database.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email address of the user, which is unique.
        hashed_password (str): The hashed password of the user.
        is_active (bool): Indicates whether the user is active.
        avatar (str): The URL of the user's avatar (optional).
        role_id (int): The foreign key linking to the Role table (optional).
        role (Role): The relationship to the Role model.
        contacts (list[Contact]): The relationship to the Contact model, representing the user's contacts.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # avatar: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=True)
    role: Mapped["Role"] = relationship("Role", lazy="selectin")
    contacts: Mapped[list["Contact"]] = relationship("Contact", back_populates="owner")
