from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings.settings import Settings


engine = create_async_engine(Settings.DB_URL, future=True, echo=True)
test_engine = create_async_engine(
    Settings.TEST_DB_URL, future=True, echo=True, poolclass=NullPool
)


async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

test_session = sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
