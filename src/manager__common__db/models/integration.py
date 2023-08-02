from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from db_utils.model.base_user_log_model import BaseUserLogModel


class Integration(BaseUserLogModel):
    __tablename__ = 'integration'

    organization_id = db.Column(UUID(as_uuid=True), nullable=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey("project.id"))
    has_confluence = db.Column(db.Boolean(), nullable=True)
    confluence_url = db.Column(db.String(1000), nullable=True)
    has_jira = db.Column(db.Boolean(), nullable=True)
    jira_url = db.Column(db.String(1000), nullable=True)
    has_gitlab = db.Column(db.Boolean(), nullable=True)
    gitlab_url = db.Column(db.String(1000), nullable=True)
    has_trello = db.Column(db.Boolean(), nullable=True)
    trello_url = db.Column(db.String(1000), nullable=True)
    has_ips = db.Column(db.Boolean(), nullable=True)
    ips_url = db.Column(db.String(1000), nullable=True)
    has_teams = db.Column(db.Boolean(), nullable=True)
    teams_url = db.Column(db.String(1000), nullable=True)
    has_enterprise = db.Column(db.Boolean(), nullable=True)
    enterprise_url = db.Column(db.String(1000), nullable=True)
    has_kiwi = db.Column(db.Boolean(), nullable=True)
    kiwi_url = db.Column(db.String(1000), nullable=True)
