"""add: intial models

Revision ID: 9cb1ccb7f588
Revises:
Create Date: 2024-10-23 01:20:27.275235

"""

import sqlalchemy as sa

from alembic import op

revision = "9cb1ccb7f588"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "human",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_human_deleted_at"), "human", ["deleted_at"], unique=False)
    op.create_table(
        "pet",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pet_deleted_at"), "pet", ["deleted_at"], unique=False)
    op.create_table(
        "soul_mates",
        sa.Column("pet_id", sa.UUID(), nullable=False),
        sa.Column("human_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["human_id"], ["human.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["pet_id"], ["pet.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("pet_id", "human_id"),
    )


def downgrade() -> None:
    op.drop_table("soul_mates")
    op.drop_index(op.f("ix_pet_deleted_at"), table_name="pet")
    op.drop_table("pet")
    op.drop_index(op.f("ix_human_deleted_at"), table_name="human")
    op.drop_table("human")
