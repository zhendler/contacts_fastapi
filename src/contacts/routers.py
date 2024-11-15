from alembic.util import status
from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.contacts.repos import ContactRepository
from src.contacts.schema import Contact, ContactResponse, ContactCreate

router =APIRouter()


@router.get("/all")
async def get_contacts(skip: int = None, limit: int = Query(default=10,le=100, ge=10)):
    return{"contacts": f"all contacts , skip - {skip} , limit: {limit}"}


@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    return await contact_repo.create_contact(contact)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contacts(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
