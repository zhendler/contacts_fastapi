from sqlalchemy import select

from src.auth.models import User, Role
from src.auth.path_utils import get_password_hash
from src.auth.schema import UserCreate, RoleEnum


class UserRepository:
    """
        Repository class for managing user-related database operations.

        Attributes:
            session: Database session for executing queries.
        """

    def __init__(self, session):
        self.session = session

        """
        Initializes the UserRepository with a database session.

        Args:
            session: Database session for query execution.
        """

    async def create_user(self, user_create: UserCreate):
        """
        Creates a new user in the database.

        Args:
            user_create (UserCreate): User data for creating a new user.

        Returns:
            User: The newly created user instance.
        """
        hashed_password = get_password_hash(user_create.password)
        user_role = await RoleRepository(self.session).get_role_by_name(RoleEnum.USER)
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            role_id = user_role.id,
            is_active = False
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_user_by_email(self, email):
        """
        Retrieves a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User or None: The user instance if found, otherwise None.
        """

        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username):
        """
        Retrieves a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User or None: The user instance if found, otherwise None.
        """

        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id):
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User or None: The user instance if found, otherwise None.
        """
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def activate_user(self, user: User):
        """
        Activates a user account.

        Args:
            user (User): The user instance to activate.

        Returns:
            None
        """
        user.is_active = True
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)


class RoleRepository:
    def __init__(self, session):
        self.session = session

    async def get_role_by_name(self, name: RoleEnum):
        query = select(Role).where(Role.name == name.value)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()