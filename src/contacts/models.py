from operator import index

from sqlalchemy import String, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base


class Contact(Base):
    __tablename__ = "contacts"

    id:Mapped[int] = mapped_column(Integer,primary_key=True, index=True)
    first_name:Mapped[str] = mapped_column(String, index=True)
    last_name:Mapped[str] = mapped_column(String, index=True)
    email:Mapped[str] = mapped_column(String, unique=True, index=True)
    phone_number:Mapped[str] = mapped_column(String, index=True)
    b_date:Mapped[str] = mapped_column(Date)
    additional_info:Mapped[str | None] = mapped_column(String, nullable=True)
    owner_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    owner: Mapped["User"] = relationship("User", back_populates="contacts", lazy="selectin")