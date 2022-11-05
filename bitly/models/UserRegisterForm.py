import re
from typing import List, Optional

from fastapi import Request

from .constants import FormatError
from ..models.models import UserRegister
from ..utilities import PasswordHelper


class UserRegisterForm:
    is_valid: bool = False

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.password_confirmation: Optional[str] = None

    async def load_data(self):
        body = await self.request.json()
        if not isinstance(body, dict):
            self.errors.append(FormatError.NOT_DICTIONARY)
            self.is_valid = False
            return
        self.username = body.get("username")
        self.email = body.get("email")
        self.password = body.get("password")
        self.password_confirmation = body.get("password_confirmation")

        self.is_valid = self.__is_valid()

    def __is_valid(self) -> bool:
        # username
        if not self.username:
            self.errors.append("Username is required.")
        elif not 5 <= len(self.username) <= 30:
            self.errors.append("Username should be min 5 characters, max 30.")
        # email
        if not self.email:
            self.errors.append("Email is required.")
        elif not self.__is_email(self.email):
            self.errors.append("Invalid Email format.")
        elif len(self.email) > 100:
            self.errors.append(f"Email is too long - {len(self.email)}. Max 100 characters.")  # really?
        # password
        if not self.password:
            self.errors.append("Password is required.")
        elif not 5 <= len(self.password) <= 24:
            self.errors.append("Password should be min 5 characters max 24.")
        # passwords match
        if self.password != self.password_confirmation:
            self.errors.append("The password confirmation does not match.")

        if self.errors:
            return False
        return True

    def get_mapped_user(self) -> UserRegister:
        return self.__map_user_data()

    def __is_email(self, email: str):
        return re.match("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email)

    def __map_user_data(self) -> UserRegister:
        user = UserRegister()
        user.username = self.username
        user.email = self.email
        user.password = PasswordHelper.get_hashed_password(self.password)
        return user
