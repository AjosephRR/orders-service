"""add customer_name to orders

Revision ID: 7b917d4cbf91
Revises: 806cd4639b90
Create Date: 2026-06-05 00:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7b917d4cbf91"
down_revision = "806cd4639b90"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "orders",
        sa.Column("customer_name", sa.String(length=100), nullable=True),
    )


def downgrade():
    op.drop_column("orders", "customer_name")
