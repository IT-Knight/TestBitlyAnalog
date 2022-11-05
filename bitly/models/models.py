from typing import Tuple
from uuid import UUID


class TokenSchema:
    access_token: str
    refresh_token: str


class TokenPayload:
    sub: str = None
    exp: int = None


class User:
    """
    pydantic validation not really good for mvc
    """
    id: UUID = UUID(int=0)
    username: str = None
    email: str = None
    password: str = None
    hashed_password: str = None


class UserAuth(User):
    ...


# @as_form
class UserRegister(User):
    password_confirmation: str = None

    @property
    def registration_data(self) -> Tuple[str, str, str]:
        return self.username, self.email, self.password


class UserOut:
    id: UUID
    email: str


class SystemUser(UserOut):
    password: str
