from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactsBase(BaseModel):
    """
    Base model for contact information.

    Attributes:
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (EmailStr): The email address of the contact.
        phone_number (str): The phone number of the contact.
        birthday (date): The birthday of the contact.
        additional_info (Optional[str]): Additional information about the contact (optional).
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None


class ContactsCreate(ContactsBase):
    """
    Model for creating a new contact.

    This model inherits all attributes from ContactsBase.
    """
    pass


class ContactsUpdate(ContactsBase):
    """
    Model for updating an existing contact.

    This model inherits all attributes from ContactsBase.
    """
    pass


class ContactsResponse(ContactsBase):
    """
    Model for the response when retrieving a contact.

    Attributes:
        id (int): The unique identifier of the contact.
    """
    id: int

    class Config:
        """
        Configuration for the Pydantic model.

        Attributes:
            from_attributes (bool): Whether to use attributes from the model's class.
        """
        from_attributes = True