import asyncio
from functools import lru_cache
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from .settings import DatabaseSettings

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.ext.asyncio import AsyncEngine


@lru_cache
def cached_session_provider(settings: "DatabaseSettings") -> "async_scoped_session":
    engine: "AsyncEngine" = create_async_engine(
        settings.engine_url, **settings.engine_kwargs
    )

    return async_scoped_session(
        async_sessionmaker(engine, class_=AsyncSession),
        asyncio.current_task,
    )
