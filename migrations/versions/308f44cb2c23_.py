"""empty message

Revision ID: 308f44cb2c23
Revises: 
Create Date: 2021-11-01 10:43:03.399470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '308f44cb2c23'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fname', sa.String(length=40), nullable=False),
    sa.Column('lname', sa.String(length=40), nullable=False),
    sa.Column('customer_no', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=40), nullable=True),
    sa.Column('offer', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_no'], ['table1.real_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('table2')
    # ### end Alembic commands ###
