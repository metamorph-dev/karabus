"""add_busses

Revision ID: beee1e081328
Revises: 3640613f55ec
Create Date: 2023-07-10 13:20:24.210588

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "beee1e081328"
down_revision = "3640613f55ec"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "busses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("color", sa.Enum("RED", "GREEN", "BLUE", name="color"), nullable=False),
        sa.Column("seats_quantity", sa.SmallInteger(), nullable=False),
        sa.Column("number_plate", sa.String(length=8), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("number_plate"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("busses")
    # ### end Alembic commands ###
