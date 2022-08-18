from aiohttp import web
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, insert,
                        select)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


async def init_db(app: web.Application):
    engine = create_async_engine(
        "postgresql+asyncpg://db_user:db_password@localhost/aiohhtpdb",
        echo=True,
    )

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    app["db"] = async_session
    yield
    await engine.dispose()


__all__ = [
    "Column",
    "ForeignKey",
    "Integer",
    "String",
    "relationship",
    "Boolean",
    "init_db",
    "select",
    "insert",
]
