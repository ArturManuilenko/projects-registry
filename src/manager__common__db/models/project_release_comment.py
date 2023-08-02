from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from db_utils.model.base_user_log_model import BaseUserLogModel


class ProjectReleaseComment(BaseUserLogModel):
    __tablename__ = 'project_release_comment'

    project_step_id = db.Column(UUID(as_uuid=True), db.ForeignKey("project_release.id"), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
