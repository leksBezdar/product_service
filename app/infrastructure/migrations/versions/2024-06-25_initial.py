"""Initial with merged revisions

Revision ID: 2a1a67583847
Revises: 
Create Date: 2024-06-28 15:30:52.125813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a1a67583847'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('oid', sa.String(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), server_default=sa.text('NULL'), nullable=True),
    sa.PrimaryKeyConstraint('oid'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_oid'), 'users', ['oid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_oid'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
