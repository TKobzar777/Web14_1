from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from src.auth.models import User, Role
from src.auth.schemas import UserCreate, RoleEnum
from src.auth.password_utils import get_password_hash


class UserRepository:
    """
    Repository class for managing user-related database operations.
    """
    def __init__(self, session: AsyncSession):
        """
        Initialize the UserRepository with an asynchronous session.

        :param session: An asynchronous session instance.
        """
        self.session = session

    async def create_user(self, user_create: UserCreate) -> User:
        """
        Create a new user with the provided details.

        :param user_create: A UserCreate schema instance containing the user details.
        :return: The created User instance.
        """
        hashed_password = get_password_hash(user_create.password)
        user_role = await RoleRepository(self.session).get_role_by_name(RoleEnum.USER)
        new_user = User(
            # username=user_create.username,
            email=user_create.email,
            role_id=user_role.id,
            hashed_password=hashed_password,
            is_active=False,  # User is active by default, you can add more logic here to handle user activation/deactivation.
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_user(self, email: str) -> User:
        """
        Retrieve a user by their email address.

        :param email: The email address of the user to retrieve.
        :return: The User instance if found, otherwise None.
        """
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def activate_user(self, user: User):
        """
        Activate the specified user.

        :param user: The User instance to activate.
        """
        user.is_active = True
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

    async def update_avatar(self, url, user: User):
        """
        Update the avatar URL for the specified user.

        :param url: The new avatar URL.
        :param user: The User instance to update.
        """
        user.avatar = url
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

class RoleRepository:
    """
    Repository class for managing role-related database operations.
    """
    def __init__(self, session: AsyncSession):
        """
        Initialize the RoleRepository with an asynchronous session.

        :param session: An asynchronous session instance.
        """
        self.session = session

    async def get_role_by_name(self, rolename: RoleEnum) -> Role:
        """
        Retrieve a role by its name.

        :param rolename: The name of the role to retrieve.
        :return: The Role instance if found, otherwise None.
        """
        query = select(Role).where(Role.name == rolename)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()