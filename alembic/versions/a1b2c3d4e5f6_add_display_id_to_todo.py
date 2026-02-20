"""add display_id to todo table

Adds a per-user sequential display_id column to the shared 'todo' table.
Existing rows are backfilled using ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id).

Revision ID: a1b2c3d4e5f6
Revises: f7f1446ee57d
Create Date: 2026-02-17

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "f7f1446ee57d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add nullable column first (safe for existing rows)
    op.add_column("todo", sa.Column("display_id", sa.Integer(), nullable=True))

    # 2. Backfill existing rows with per-user sequential numbers
    #    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id) gives stable,
    #    user-scoped sequential IDs matching insertion order.
    op.execute(
        """
        WITH ranked AS (
            SELECT
                id,
                ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id) AS rn
            FROM todo
        )
        UPDATE todo
        SET display_id = ranked.rn
        FROM ranked
        WHERE todo.id = ranked.id
        """
    )

    # 3. Create index for fast (user_id, display_id) lookups
    op.create_index("ix_todo_display_id", "todo", ["display_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_todo_display_id", table_name="todo")
    op.drop_column("todo", "display_id")
