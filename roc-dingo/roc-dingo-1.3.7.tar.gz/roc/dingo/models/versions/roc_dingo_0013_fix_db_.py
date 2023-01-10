# -*- coding: utf-8 -*-
"""Fix database discrepancy with model

Revision ID: roc_dingo_0010b_fix_db
Revises: roc_dingo_0010_add_view
Create Date: 2021-07-20 13:56:44.889371

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0013_fix_db'
down_revision = 'roc_dingo_0012_add_data'
branch_labels = None
depends_on = None


def upgrade():

    op.execute('COMMIT')
    # state columns type should be of type file_state_list
    # (and not file_state_type)
    op.execute('DROP TYPE IF EXISTS file_state_list')
    op.execute('ALTER TYPE file_state_type RENAME TO file_state_list')

    # idem for status
    op.execute('DROP TYPE IF EXISTS file_status_list')
    op.execute('ALTER TYPE file_status_type RENAME TO file_status_list')


def downgrade():
    op.execute('COMMIT')
    op.execute('ALTER TYPE file_state_list RENAME TO file_state_type')
    op.execute('ALTER TYPE file_status_list RENAME TO file_status_type')
