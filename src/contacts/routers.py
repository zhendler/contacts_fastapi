from fastapi import APIRouter, Query, Path, HTTPException, status
from fastapi.params import Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from config.cache import invalidate_get_contacts_repo_cache
from config.db import get_db
from src.auth.models import User
from src.auth.schema import RoleEnum
from src.auth.utils import get_current_user, RoleChecker
from src.contacts.repos import ContactRepository
from src.contacts.schema import Contact, ContactResponse, ContactCreate, ContactUpdate, ContactSearch

router =APIRouter()


@router.get("/all", response_model=list[ContactResponse], dependencies=[Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))])
async def get_contacts(
        skip: int = 0,
        limit: int = 10,
        user: User = Depends (get_current_user),
        db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_all_contacts(user.id, skip, limit)
    return contacts


@router.get("/upcoming_birthdays", response_model=list[ContactResponse], dependencies=[Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))])
async def get_upcoming_birthdays(
        user: User = Depends (get_current_user),
        db: AsyncSession = Depends(get_db)):
    """
        Retrieve a list of contacts with upcoming birthdays for the current user.

        This endpoint fetches contacts whose birthdays are approaching, based on the user's data.

        Args:
            user (User): The currently authenticated user, provided by `get_current_user`.
            db (AsyncSession): The database session, provided by `get_db`.

        Returns:
            List[ContactResponse]: A list of contact details formatted as `ContactResponse`.

        Access Control:
            - Roles allowed: ADMIN, USER
        """
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_upcoming_birthdays(user.id)
    return [ContactResponse.model_validate(contact, from_attributes=True) for contact in contacts]

@router.post("/", response_model=ContactResponse,
             status_code=status.HTTP_201_CREATED,
             dependencies= [Depends(RateLimiter(times=5, seconds=60)),
                            Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))])
async def create_contact(contact: ContactCreate,
                        user: User = Depends (get_current_user),
                        db:AsyncSession = Depends(get_db)):
    """
        Create a new contact for the current user.

        This endpoint allows the user to add a new contact to their personal list.

        Args:
            contact (ContactCreate): The data for the new contact, provided in the request body.
            user (User): The currently authenticated user, provided by `get_current_user`.
            db (AsyncSession): The database session, provided by `get_db`.

        Returns:
            ContactResponse: The newly created contact's details, formatted as `ContactResponse`.

        Access Control:
            - Roles allowed: ADMIN, USER
        Rate Limiting:
            - Maximum 5 requests per minute.
        """
    contact_repo = ContactRepository(db)
    await invalidate_get_contacts_repo_cache(user.id)

    return await contact_repo.create_contact(contact, user.id)




@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))])
async def update_contact(contact_id: int,
                         contact_data: ContactUpdate,
                         user: User = Depends (get_current_user),
                         db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contact(contact_id, user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    await invalidate_get_contacts_repo_cache(user.id)
    updated_contact = await contact_repo.update_contact(contact_id, contact_data.dict(exclude_unset=True))
    return updated_contact

@router.delete("/{contact_id}", status_code=204, dependencies=[Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))])
async def delete_contact(contact_id: int,
                         user: User = Depends (get_current_user),
                         db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    await invalidate_get_contacts_repo_cache(user.id)
    result = await contact_repo.delete_contact(contact_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")




@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))])
async def get_contact(contact_id: int,
                        user: User = Depends (get_current_user),
                        db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contact(contact_id, user.id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact





@router.post("/search/{search_term}", response_model= list[ContactResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))])
async def get_searched_contact( search:ContactSearch,
                            user: User = Depends (get_current_user),
                            db:AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    search_result = await contact_repo.get_search_result(search, user.id)
    if not search_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return [ContactResponse.model_validate(contact, from_attributes=True) for contact in search_result]


