# -*- coding: utf-8; -*-
"""add work orders

Revision ID: 62cfde95d655
Revises: 9c111f4b5451
Create Date: 2022-08-09 19:43:01.326910

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = '62cfde95d655'
down_revision = '9c111f4b5451'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types


workorder_id_seq = sa.Sequence('workorder_id_seq')


def upgrade():
    from sqlalchemy.schema import CreateSequence

    # id sequence
    op.execute(CreateSequence(workorder_id_seq))

    # workorder
    op.create_table('workorder',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('customer_uuid', sa.String(length=32), nullable=False),
                    sa.Column('date_submitted', sa.Date(), nullable=True),
                    sa.Column('date_received', sa.Date(), nullable=True),
                    sa.Column('date_released', sa.Date(), nullable=True),
                    sa.Column('date_delivered', sa.Date(), nullable=True),
                    sa.Column('notes', sa.Text(), nullable=True),
                    sa.Column('status_code', sa.Integer(), nullable=False),
                    sa.Column('status_text', sa.String(length=255), nullable=True),
                    sa.ForeignKeyConstraint(['customer_uuid'], ['customer.uuid'], name='workorder_fk_customer'),
                    sa.PrimaryKeyConstraint('uuid')
    )

    # workorder_event
    op.create_table('workorder_event',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('workorder_uuid', sa.String(length=32), nullable=False),
                    sa.Column('type_code', sa.Integer(), nullable=False),
                    sa.Column('occurred', sa.DateTime(), nullable=False),
                    sa.Column('user_uuid', sa.String(length=32), nullable=False),
                    sa.Column('note', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], name='workorder_event_fk_user'),
                    sa.ForeignKeyConstraint(['workorder_uuid'], ['workorder.uuid'], name='workorder_event_fk_workorder'),
                    sa.PrimaryKeyConstraint('uuid')
    )


def downgrade():
    from sqlalchemy.schema import DropSequence

    # workorder_event
    op.drop_table('workorder_event')

    # workorder
    op.drop_table('workorder')

    # id sequence
    op.execute(DropSequence(workorder_id_seq))
