"""empty message

Revision ID: 9c7440e7b737
Revises: d678bb85df23
Create Date: 2021-11-30 11:52:19.431637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c7440e7b737'
down_revision = 'd678bb85df23'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE categoryproject RENAME VALUE 'oto' TO 'stands_installations__putting_into_production';")
    op.execute("ALTER TYPE categoryproject RENAME VALUE 'middle_network_layer' TO 'base_station';")
    op.execute("ALTER TYPE categoryproject RENAME VALUE 'communication_technologies' TO 'routers_uspd';")
    op.execute("ALTER TYPE categoryproject RENAME VALUE 'upper_level_or_private_office' TO 'applications';")

    op.execute("ALTER TYPE categoryproject ADD VALUE 'calibration_installations';")
    op.execute("ALTER TYPE categoryproject ADD VALUE 'external_projects';")
    op.execute("ALTER TYPE categoryproject ADD VALUE 'heat_metering';")
    op.execute("ALTER TYPE categoryproject ADD VALUE 'infrastructure_projects';")
    op.execute("ALTER TYPE categoryproject ADD VALUE 'modems';")


def downgrade():
    op.execute("ALTER TYPE categoryproject RENAME VALUE 'stands_installations__putting_into_production' TO 'oto';")
    op.execute("ALTER TYPE categoryproject RENAME VALUE 'base_station' TO 'middle_network_layer';")
    op.execute("ALTER TYPE categoryproject RENAME VALUE 'routers_uspd' TO 'communication_technologies';")
    op.execute("ALTER TYPE categoryproject RENAME VALUE 'applications' TO 'upper_level_or_private_office';")
