"""property_model

Revision ID: b4f0f81e6797
Revises: 
Create Date: 2024-06-12 12:58:21.404514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4f0f81e6797'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('properties',
    sa.Column('propertyid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('city', sa.String(length=255), nullable=False),
    sa.Column('state', sa.String(length=5), nullable=False),
    sa.Column('zipcode', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('bedrooms', sa.Integer(), nullable=True),
    sa.Column('bathrooms', sa.Integer(), nullable=True),
    sa.Column('squarefeet', sa.Integer(), nullable=True),
    sa.Column('geometry', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('propertyid')
    )
    op.create_index(op.f('ix_properties_city'), 'properties', ['city'], unique=False)
    op.create_index(op.f('ix_properties_propertyid'), 'properties', ['propertyid'], unique=False)
    op.create_index(op.f('ix_properties_state'), 'properties', ['state'], unique=False)
    op.create_index(op.f('ix_properties_zipcode'), 'properties', ['zipcode'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_properties_zipcode'), table_name='properties')
    op.drop_index(op.f('ix_properties_state'), table_name='properties')
    op.drop_index(op.f('ix_properties_propertyid'), table_name='properties')
    op.drop_index(op.f('ix_properties_city'), table_name='properties')
    op.drop_table('properties')
    # ### end Alembic commands ###