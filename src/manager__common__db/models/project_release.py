from datetime import datetime

from db_utils.model.base_user_log_model import BaseUserLogModel
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID
from src.manager__common__db.utils.project_release_stasus import StatusRelease


class ProjectRelease(BaseUserLogModel):
    __tablename__ = 'project_release'
    organization_id = db.Column(UUID(as_uuid=True), nullable=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey("project.id"))
    name = db.Column(db.String(255), nullable=False)
    date_started = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    date_finished_planned = db.Column(db.DateTime(), nullable=False)
    date_finished_real = db.Column(db.DateTime(), nullable=True)
    description = db.Column(db.String(2000), nullable=True)
    conversation_url = db.Column(db.String(1000), nullable=True)
    release_scope_url = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.Enum(StatusRelease), nullable=False)

    def __repr__(self) -> str:
        return f'<ProjectRelease {self.name}>'
