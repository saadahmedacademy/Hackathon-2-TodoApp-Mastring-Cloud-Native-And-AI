"""auto display_id trigger and backfill nulls

Permanently fixes display_id inconsistency between Phase-2 and Phase-3:

  1. Backfills any rows where display_id IS NULL using ROW_NUMBER() OVER
     (PARTITION BY user_id ORDER BY created_at).

  2. Creates a PostgreSQL BEFORE INSERT trigger that auto-assigns display_id
     when a row is inserted without it (i.e. Phase-2 inserts).

After this migration runs:
  - Every existing NULL display_id is filled.
  - All future inserts from ANY client (Phase-2, Phase-3, direct SQL) will
    automatically receive a per-user sequential display_id.

Revision ID: b2c3d4e5f6a7
Revises: ea4a63f9e4be
Create Date: 2026-02-18

"""
from typing import Sequence, Union

from alembic import op

revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "ea4a63f9e4be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Step 1: Backfill all rows that still have display_id IS NULL ─────────
    # Uses ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) so the
    # numbers are stable, user-scoped, and match insertion order.
    op.execute(
        """
        UPDATE todo t
        SET display_id = sub.rn
        FROM (
            SELECT id,
                   ROW_NUMBER() OVER (
                       PARTITION BY user_id
                       ORDER BY created_at
                   ) AS rn
            FROM todo
        ) sub
        WHERE t.id = sub.id
          AND t.display_id IS NULL
        """
    )

    # ── Step 2: Create trigger function ──────────────────────────────────────
    # Fires BEFORE every INSERT on the todo table.
    # If the caller (Phase-2, Phase-3, raw SQL) supplies NULL for display_id,
    # the trigger computes MAX(display_id)+1 for that user and fills it in.
    # If the caller already supplied a display_id (Phase-3), the value is kept.
    op.execute(
        """
        CREATE OR REPLACE FUNCTION assign_todo_display_id()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.display_id IS NULL THEN
                SELECT COALESCE(MAX(display_id), 0) + 1
                INTO   NEW.display_id
                FROM   todo
                WHERE  user_id = NEW.user_id;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    # ── Step 3: Attach trigger to todo table ─────────────────────────────────
    # DROP IF EXISTS first so this migration is idempotent / re-runnable.
    op.execute(
        """
        DROP TRIGGER IF EXISTS todo_display_id_trigger ON todo;
        """
    )
    op.execute(
        """
        CREATE TRIGGER todo_display_id_trigger
        BEFORE INSERT ON todo
        FOR EACH ROW
        EXECUTE FUNCTION assign_todo_display_id();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS todo_display_id_trigger ON todo;")
    op.execute("DROP FUNCTION IF EXISTS assign_todo_display_id();")
    # Note: we do NOT null-out display_id on downgrade — data is preserved.
