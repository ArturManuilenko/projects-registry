from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from db_utils.model.base_user_log_model import BaseUserLogModel


class Modification(BaseUserLogModel):
    __tablename__ = 'modification'

    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey("project.id"))
    organization_id = db.Column(UUID(as_uuid=True), nullable=True)
    name = db.Column(db.String(255), nullable=False)
