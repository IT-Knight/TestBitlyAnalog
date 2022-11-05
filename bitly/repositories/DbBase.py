from typing import Any
from uuid import uuid1
from psycopg2 import connect

from ..models.constants import EnvVariable
from ..utilities import db_try_except
from decouple import config

db_config = {
    "host": config(EnvVariable.DB_HOST),
    "dbname": config(EnvVariable.DB_NAME),
    "user": config(EnvVariable.DB_USER),
    "password": config(EnvVariable.DB_PASSWORD),
    "port": config(EnvVariable.DB_PORT)
}


class DbException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors


class DbBase:

    @db_try_except
    @staticmethod
    async def execute_query(sql: str, *args) -> list[tuple[Any, ...]]:
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, args)
                print(cur.query)
                return cur.fetchall()

    @db_try_except
    @staticmethod
    async def execute_command(sql: str, *args) -> bool:
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, *args)
                conn.commit()
                return cur.rowcount != 0

    # def __close(self):
    #     if self.__conn:
    #         try:
    #             self.__conn.close()
    #         except Exception as e:
    #             raise DbException(*e.args)
    #
    # def __exit__(self, type_, value, traceback):
    #     # can test for type and handle different situations
    #     self.__close()
