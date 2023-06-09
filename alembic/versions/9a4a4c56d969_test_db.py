"""test db

Revision ID: 9a4a4c56d969
Revises: 
Create Date: 2023-05-18 19:39:42.276750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a4a4c56d969'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_code'), 'categories', ['code'], unique=False)
    op.create_table('file_uploads',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email_add', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('file_type', sa.String(), nullable=True),
    sa.Column('first_content', sa.Text(), nullable=True),
    sa.Column('last_content', sa.Text(), nullable=True),
    sa.Column('file_path', sa.String(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_uploads_email_add'), 'file_uploads', ['email_add'], unique=False)
    op.create_table('diagnosis',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('category_id', sa.UUID(), nullable=False),
    sa.Column('diag_code', sa.String(), nullable=True),
    sa.Column('full_code', sa.String(), nullable=True),
    sa.Column('abb_desc', sa.String(), nullable=True),
    sa.Column('full_desc', sa.String(), nullable=True),
    sa.Column('file_upload_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['file_upload_id'], ['file_uploads.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('file_upload_id')
    )
    op.create_index(op.f('ix_diagnosis_diag_code'), 'diagnosis', ['diag_code'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_diagnosis_diag_code'), table_name='diagnosis')
    op.drop_table('diagnosis')
    op.drop_index(op.f('ix_file_uploads_email_add'), table_name='file_uploads')
    op.drop_table('file_uploads')
    op.drop_index(op.f('ix_categories_code'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
