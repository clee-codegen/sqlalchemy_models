import datetime
from functools import lru_cache, partial
from typing import TYPE_CHECKING, Annotated, TypeAlias
from uuid import UUID

from sqlalchemy import DateTime, Index, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_base,
    declarative_mixin,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any

    from sqlalchemy import Table


timestamp: TypeAlias = Annotated[
    datetime.datetime,
    mapped_column(DateTime(timezone=True)),
]

base_relationship = partial(relationship, viewonly=True, lazy="noload")


@declarative_mixin
class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=func.gen_random_uuid()
    )


@declarative_mixin
class AuditMixin:
    __tablename__: str
    __table_args__: "tuple[Any, ...]" = tuple()

    created_at: Mapped[timestamp] = mapped_column(
        nullable=False, server_default=func.clock_timestamp()
    )
    updated_at: Mapped[timestamp] = mapped_column(
        server_default=func.clock_timestamp(), nullable=False
    )
    deleted_at: Mapped[timestamp | None] = mapped_column(index=True)

    def __init_subclass__(cls, search: bool = False) -> None:
        if search:
            table_name: str = cls.__tablename__
            table_args: "tuple[Any, ...]" = getattr(cls, "__table_args__", tuple())
            table_args += (Index(f"idx_{table_name}_updated_at", cls.updated_at),)
            cls.__table_args__ = table_args

        return super().__init_subclass__()


def create_non_deleted_unique_contraint(*column: str) -> "Index":
    return Index(
        f"idx_{'_'.join(column)}",
        *column,
        unique=True,
        postgresql_where="deleted_at is null",
    )


class SQLBaseModel(DeclarativeBase, AuditMixin, UUIDMixin):
    # Allows us to define relationships later with annotated fields in the model
    __allow_unmapped__ = True

    def __init_subclass__(cls, **kwargs) -> None:
        if not hasattr(cls, "__tablename__"):
            raise ValueError("SQLBaseModel must be provided __tablename__")

        super().__init_subclass__(**kwargs)

    @classmethod
    @lru_cache(maxsize=1)
    def get_table(cls) -> "Table":
        return cls.registry.metadata.tables[cls.__tablename__]


BareBase = declarative_base(metadata=SQLBaseModel.metadata)
