from passlib.context import CryptContext
from psycopg2 import Error as PsycopgError


class db_try_except:

    def __init__(self, func=None, logger=None):
        self.func = func
        self.logger = logger

    def __call__(self, *args, **kwargs):
        if not self.func:
            return self.__class__(args[0], logger=self.logger)

        # how to pass the instance of decorated class?
        async def wrapper(sql: str, *args2):
            try:
                return await self.func(sql, *args2)
            except (Exception, PsycopgError) as error:
                # self.logger.logError()
                print("Error while connecting to PostgreSQL", error)

        return wrapper(*args, **kwargs)


class PasswordHelper:
    __password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        return cls.__password_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls.__password_context.verify(password, hashed_password)



