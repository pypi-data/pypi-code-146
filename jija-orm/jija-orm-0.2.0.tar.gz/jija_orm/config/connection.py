import asyncio
import asyncpg


class Connection:
    def __init__(self, host, port, user, password, database):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database

    def check(self):
        asyncio.run(self.async_check())

    async def async_check(self):
        await asyncpg.connect(
            f'postgresql://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}')

    async def get_connection(self) -> asyncpg.connection.Connection:
        return await asyncpg.connect(
            f'postgresql://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}')
