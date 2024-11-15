from sqlalchemy import select

from src.contacts.models import Contact
from src.contacts.schema import ContactCreate


class ContactRepository:

    def __init__(self, session):
        self.session = session


    async def get_contacts(self, contact_id: int) -> Contact:
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, contact:ContactCreate)->Contact:
        new_contact = Contact(**contact.model_dump())
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)
        return new_contact

    def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
        db_contact = get_contact(db, contact_id)
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact