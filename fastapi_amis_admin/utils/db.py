from typing import Generator, Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker, Session


class SqlalchemyAsyncClient():

    def __init__(self, engine: AsyncEngine):
        self.engine: AsyncEngine = engine
        self.session_maker: sessionmaker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False,
                                                        autocommit=False,
                                                        autoflush=False, )

    async def session_factory(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self.session_maker() as session:
            yield session


class SqlalchemySyncClient():

    def __init__(self, engine: Engine):
        self.engine: Engine = engine
        self.session_maker = sessionmaker(self.engine, autocommit=False, autoflush=False)

    def session_factory(self) -> Generator[Session, Any, None]:
        session = self.session_maker()
        try:
            yield session
            session.commit()
        finally:
            session.close()