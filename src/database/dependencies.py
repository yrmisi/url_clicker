from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .db_config import AsyncSessionLocal


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """ """
    async with AsyncSessionLocal() as async_session:
        yield async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
