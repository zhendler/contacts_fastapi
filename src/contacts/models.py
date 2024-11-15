from operator import index

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column

from config.db import Base


class Contact(Base):
    __tablename__ = "contacts"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name:Mapped[str] = mapped_column(String, index=True)
    last_name:Mapped[str] = mapped_column(String, index=True)
    email:Mapped[str] = mapped_column(String, unique=True, index=True)
    phone_number:Mapped[str] = mapped_column(String, index=True)
    b_date:Mapped[str] = mapped_column(Date)
    additional_info:Mapped[str | None] = mapped_column(String, nullable=True)
