from sqlalchemy import select,  Date, func
from datetime import datetime, timedelta, date
# from sqlalchemy.sql.functions import now
# from src.contacts.models import Contact
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound


from src.contacts.models import Contact
from src.contacts.schemas import ContactsCreate, ContactsUpdate


class ContactRepository:

    def __init__(self, session: AsyncSession):
        """
        Initialize the ContactRepository with an asynchronous session.

        :param session: An asynchronous session instance.
        """
        self.session = session

    async def create_contact(self, contact_create: ContactsCreate, owner_id: int) -> Contact:
        """
        Create a new contact for the specified owner.

        :param contact_create: A ContactsCreate schema instance containing the contact details.
        :param owner_id: The ID of the owner for whom the contact is being created.
        :return: The created Contact instance.
        """
        new_contact = Contact(
            **contact_create.model_dump(),
            owner_id=owner_id
        )
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)
        return new_contact

    async def get_contact(self, contact_id: int, owner_id: int) -> Contact:
        """
        Retrieve a contact by its ID and owner ID.

        :param contact_id: The ID of the contact to retrieve.
        :param owner_id: The ID of the owner of the contact.
        :return: The Contact instance if found, otherwise None.
        """
        query = select(Contact).where(Contact.id == contact_id, Contact.owner_id == owner_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_contacts(self, owner_id: int, skip: int = 0, limit: int = 10) -> list[Contact]:
        """
        Retrieve a list of contacts for the specified owner with pagination.

        :param owner_id: The ID of the owner.
        :param skip: The number of contacts to skip (for pagination).
        :param limit: The maximum number of contacts to return (for pagination).
        :return: A list of Contact instances.
        """
        query = select(Contact).where(Contact.owner_id == owner_id).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()



    async def update_contact(self, contact_id: int, contact_update: ContactsUpdate, owner_id: int) -> Contact:
        """
        Update an existing contact for the specified owner.

        :param contact_id: The ID of the contact to update.
        :param contact_update: A ContactsUpdate schema instance containing the updated contact details.
        :param owner_id: The ID of the owner of the contact.
        :return: The updated Contact instance if found, otherwise None.
        """
        contact = await self.get_contact(contact_id, owner_id)
        if contact:
            for key, value in contact_update.model_dump().items():
                setattr(contact, key, value)
            await self.session.commit()
            await self.session.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int, owner_id: int):
        """
        Delete a contact by its ID and owner ID.

        :param contact_id: The ID of the contact to delete.
        :param owner_id: The ID of the owner of the contact.
        """
        contact = await self.get_contact(contact_id, owner_id)
        if contact:
            await self.session.delete(contact)
            await self.session.commit()


    async def search_contacts_birthdays(self, owner_id: int, days: int = 7):
        """
        Search for contacts whose birthdays are within the specified number of days for the specified owner.

        :param owner_id: The ID of the owner.
        :param days: The number of days to search for upcoming birthdays.
        :return: A list of Contact instances.
        """
        today = date.today()
        query = select(Contact).where(
            (Contact.owner_id == owner_id) &
            (func.date_part('doy', Contact.birthday).between(
            func.date_part('doy', func.now()),
            func.date_part('doy', func.now()) + days
            )
            )
        )

        # Выполнение запроса
        results = await self.session.execute(query)
        return results.scalars().all()

    # get_contacts_by_id
    async def get_contact_admin(self, contact_id: int) -> Contact:
        """
        Retrieve a contact by its ID for administrative purposes.

        :param contact_id: The ID of the contact to retrieve.
        :return: The Contact instance if found, otherwise None.
        """

        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    # get_contacts_admin
    async def get_contacts_admin(self, skip: int = 0, limit: int = 10) -> list[Contact]:
        """
        Retrieve a list of contacts with pagination for administrative purposes.

        :param skip: The number of contacts to skip (for pagination).
        :param limit: The maximum number of contacts to return (for pagination).
        :return: A list of Contact instances.
        """
        query = select(Contact).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def search_contacts_birthdays_admin(self, days: int = 7):
        """
        Search for contacts whose birthdays are within the specified number of days for administrative purposes.

        :param days: The number of days to search for upcoming birthdays.
        :return: A list of Contact instances.
        """
        query = select(Contact).where(
            func.date_part('doy', Contact.birthday).between(
                func.date_part('doy', func.now()),
                func.date_part('doy', func.now()) + days
            )
        )
        # Выполнение запроса
        results = await self.session.execute(query)
        return results.scalars().all()


