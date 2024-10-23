from sqlalchemy import UUID, Column, ForeignKey

from .base import BareBase, SQLBaseModel


class Pet(SQLBaseModel):
    __tablename__ = "pet"


class Human(SQLBaseModel):
    __tablename__ = "human"


class SoulMates(BareBase):
    __tablename__ = "soul_mates"

    pet_id = Column(UUID, ForeignKey("pet.id", ondelete="SET NULL"), primary_key=True)
    human_id = Column(
        UUID, ForeignKey("human.id", ondelete="SET NULL"), primary_key=True
    )
