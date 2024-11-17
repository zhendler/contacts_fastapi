from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    b_date: date
    additional_info: str|None = None

class ContactResponse(Contact):
    id: int

    class Config:
        from_attributes = True


class ContactCreate(Contact):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    b_date: Optional[date] = None
    additional_info: Optional[str] = None


class ContactSearch(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None