from sqlalchemy import Date, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base


class Contact(Base):
    """
    SQLAlchemy model representing a contact in the database.

    Attributes:
        id (int): The primary key of the contact.
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (str): The email address of the contact.
        phone_number (str): The phone number of the contact.
        birthday (Date): The birthday of the contact.
        additional_info (str | None): Additional information about the contact (optional).
        owner_id (int): The foreign key linking to the User table (optional).
        owner (User): The relationship to the User model.
    """
    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String, index=True)
    birthday: Mapped[Date] = mapped_column(Date)
    additional_info: Mapped[str | None] = mapped_column(String, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True) # Foreign key to User table
    owner: Mapped["User"] = relationship("User", back_populates="contacts")