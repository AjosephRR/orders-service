"""add order details fields

Revision ID: 0f41d7c9f6ab
Revises: 7b917d4cbf91
Create Date: 2026-06-05 00:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0f41d7c9f6ab"
down_revision = "7b917d4cbf91"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "orders",
        sa.Column("customer_email", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "orders",
        sa.Column("shipping_address", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "orders",
        sa.Column("notes", sa.String(length=500), nullable=True),
    )


def downgrade():
    op.drop_column("orders", "notes")
    op.drop_column("orders", "shipping_address")
    op.drop_column("orders", "customer_email")
