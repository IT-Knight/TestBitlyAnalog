from uuid import UUID

from ..models.models import User, UserRegister
from .DbBase import DbBase

from ..utilities.utils import PasswordHelper


class UserRepository(DbBase):

    @classmethod
    async def get_user_id(cls, email: str) -> UUID:
        res = await cls.execute_query("SELECT id FROM dbo.Users WHERE email = %s", email)
        return res[0]

    @classmethod
    async def get_by_id(cls, uuid: UUID) -> User:
        return cls.__map_fetched_user(
            await cls.execute_query("SELECT id, username, email, password FROM dbo.Users WHERE ID = %s", uuid))

    @classmethod
    async def get_by_email(cls, email: str) -> User:
        return cls.__map_fetched_user(
            await cls.execute_query(f'SELECT id, username, email, password FROM dbo.Users WHERE email = %s', email))

    @classmethod
    async def verify_email_is_present(cls, email: str) -> bool:
        return any(await cls.execute_query(f'SELECT id FROM dbo.Users WHERE email = %s', email))

    @classmethod
    async def add(cls, user_data: UserRegister) -> bool:
        return await cls.execute_command("INSERT INTO dbo.Users(username, email, password) VALUES (%s, %s, %s)",
                                         user_data.registration_data)

    @classmethod
    async def check_credentials(cls, email: str, password: str) -> bool:
        user_exists = await cls.get_by_email(email)
        if not user_exists:
            return False

        password_correct = PasswordHelper.verify_password(password)
        if not password_correct:
            return False

        return True

    @staticmethod
    def __map_fetched_user(res: list) -> User | None:
        if not (res or any(res)):
            return None

        user = User()
        user.id, user.username, user.email, user.hashed_password = res[0]
        return user




