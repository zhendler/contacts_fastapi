from fastapi import APIRouter, Query, Path, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.contacts.repos import ContactRepository
from src.contacts.schema import Contact, ContactResponse, ContactCreate, ContactUpdate, ContactSearch

router =APIRouter()


@router.get("/all")
async def get_contacts(db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_all_contacts()
    return contacts


@router.get("/upcoming_birthdays", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_upcoming_birthdays()
    return [ContactResponse.model_validate(contact, from_attributes=True) for contact in contacts]

@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    return await contact_repo.create_contact(contact)




@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact_data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    updated_contact = await contact_repo.update_contact(contact_id, contact_data.dict(exclude_unset=True))
    return updated_contact

@router.delete("/{contact_id}", status_code=204)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    result = await contact_repo.delete_contact(contact_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")




@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact





@router.post("/search/{search_term}", response_model= list[ContactResponse])
async def get_serched_contact( search:ContactSearch, db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    search_result = await contact_repo.get_search_result(search)
    if not search_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return [ContactResponse.model_validate(contact, from_attributes=True) for contact in search_result]


