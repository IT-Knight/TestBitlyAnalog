import re
from typing import List, Optional
from fastapi import Request

from bitly.models.constants import FormatError
from bitly.models.models import UserAuth
from bitly.utilities import PasswordHelper


class UserLoginForm:
    is_valid: bool = False

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        body = await self.request.json()
        if not isinstance(body, dict):
            self.errors.append(FormatError.NOT_DICTIONARY)
            self.is_valid = False
            return
        self.email = body.get("email")
        self.password = body.get("password")
        self.is_valid = self.__is_valid()
        return self

    def __is_valid(self) -> bool:
        # email
        if not self.email:
            self.errors.append("Please enter the email.")
        elif not self.__is_email(self.email) or len(self.email) > 100:
            self.errors.append("Invalid email.")
        # password
        if not self.password:
            self.errors.append("Please enter the password.")
        elif not 5 <= len(self.password) <= 24:
            self.errors.append("Invalid password.")

        if self.errors:
            return False
        return True

    def __is_email(self, email: str):
        return re.match("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email)

    # def get_mapped_user(self) -> UserAuth:
    #     return self.__map_user_data()
    #
    # def __map_user_data(self) -> UserAuth:
    #     user = UserAuth()
    #     user.email = self.email
    #     user.hashed_password = PasswordHelper.get_hashed_password(self.password)
    #     return user
