from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select, or_, extract

from src.contacts.models import Contact

from src.contacts.schema import ContactCreate, ContactUpdate, ContactResponse, ContactSearch


class ContactRepository:

    def __init__(self, session):
        self.session = session

    async def get_all_contacts(self, skip: int = None, limit: int = 10) -> list[Contact:ContactResponse]:
        query = select(Contact).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_contact(self, contact_id: int) -> Contact:
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, contact:ContactCreate)->Contact:
        new_contact = Contact(**contact.model_dump())
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)
        return new_contact

    async def update_contact(self, contact_id: int, contact_data: dict) -> Contact:
        contact_to_update = await self.session.get(Contact, contact_id)
        if not contact_to_update:
            raise HTTPException(status_code=404, detail="Contact not found")

        for key, value in contact_data.items():
            setattr(contact_to_update, key, value)

        await self.session.commit()
        await self.session.refresh(contact_to_update)
        return contact_to_update

    async def delete_contact(self, contact_id: int):
        contact_to_delete = await self.session.get(Contact, contact_id)
        if not contact_to_delete:
            raise HTTPException(status_code=404, detail="Contact not found")

        await self.session.delete(contact_to_delete)
        await self.session.commit()

    async def get_search_result(self, search: ContactSearch) -> list[Contact]:
        query = select(Contact)
        filters = []
        if search.first_name:
            filters.append(Contact.first_name.contains(search.first_name))
        if search.last_name:
            filters.append(Contact.last_name.contains(search.last_name))
        if search.email:
            filters.append(Contact.email.contains(search.email))

        if filters:
            query = query.where(or_(*filters))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_upcoming_birthdays(self) -> list[Contact]:
        today = date.today()
        week_later = today + timedelta(days=7)

        query = select(Contact).where(
            or_(
                extract('month', Contact.b_date) == today.month,
                extract('month', Contact.b_date) == week_later.month
            ),
            or_(
                extract('day', Contact.b_date) >= today.day,
                extract('day', Contact.b_date) <= week_later.day
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

