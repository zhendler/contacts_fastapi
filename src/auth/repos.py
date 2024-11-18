from dns.e164 import query
from sqlalchemy import select

from src.auth.models import User
from src.auth.path_utils import get_password_hash
from src.auth.schema import UserCreate


class UserRepository:

    def __init__(self, session):
        self.session = session

    async def create_user(self, user_create: UserCreate):
        hashed_password = get_password_hash(user_create.password)
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_user_by_email(self, email):
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username):
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()