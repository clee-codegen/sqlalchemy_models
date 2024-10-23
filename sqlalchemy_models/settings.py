from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_", frozen=True)
    host: str = "db"
    port: int = 5432
    user: str = "dbuser"
    password: str = "development"
    dialect: str = "postgresql+asyncpg"
    db: str = "db"

    echo: bool = False
    pool_size: int = 20
    max_overflow: int = 20
    pool_timeout: int = 5

    @property
    def engine_url(self) -> str:
        return (
            f"{self.dialect}://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )

    @property
    def engine_kwargs(self) -> "dict[str, Any]":
        return {
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "pool_timeout": self.pool_timeout,
            "echo": self.echo,
        }
