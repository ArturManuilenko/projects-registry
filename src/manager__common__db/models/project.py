from db_utils.modules.custom_query import CustomQuery
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from src.manager__common__db.models.integration import Integration
from src.manager__common__db.models.modification import Modification
from db_utils.model.base_user_log_model import BaseUserLogModel
from src.manager__common__db.models.project_release import ProjectRelease
from src.manager__common__db.utils.category_enum import CategoryProject
from src.manager__common__db.utils.priority_enum import PriorityProject
from src.manager__common__db.utils.status_enum import StatusProject
from src.manager__common__db.utils.type_enum import TypeProject


class Project(BaseUserLogModel):
    __tablename__ = 'project'
    name = db.Column(db.String(255), unique=True, nullable=False)
    key = db.Column(db.String(5), unique=True, nullable=False)
    project_manager_user_id = db.Column(UUID(as_uuid=True), nullable=False)
    date_launched = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.Enum(StatusProject), nullable=False)
    is_initiative_document_exists = db.Column(db.Boolean(), nullable=False)
    is_archived = db.Column(db.Boolean(), default=False)
    notes = db.Column(db.String, nullable=True)
    type = db.Column(db.Enum(TypeProject), nullable=False)
    priority = db.Column(db.Enum(PriorityProject), nullable=False)
    organization_id = db.Column(UUID(as_uuid=True), nullable=True)
    customer_organization_id = db.Column(UUID(as_uuid=True), nullable=True)
    executor_organization_id = db.Column(UUID(as_uuid=True), nullable=True)
    category = db.Column(db.Enum(CategoryProject), nullable=False)

    @declared_attr
    def modifications(self) -> Modification:
        return db.relationship(
            'Modification',
            primaryjoin=f"and_({Modification.__name__}.project_id=={self.__name__}.id, {Modification.__name__}.is_alive=='true')",
            query_class=CustomQuery,
        )

    @declared_attr
    def integration(self) -> Integration:
        return db.relationship(
            'Integration',
            primaryjoin=f"and_({Integration.__name__}.project_id=={self.__name__}.id, {Integration.__name__}.is_alive=='true')",
            uselist=False,
        )

    @declared_attr
    def releases(self) -> ProjectRelease:
        return db.relationship(
            'ProjectRelease',
            primaryjoin=f"and_({ProjectRelease.__name__}.project_id=={self.__name__}.id, {ProjectRelease.__name__}.is_alive=='true')",
            order_by='desc(ProjectRelease.date_created)',
            query_class=CustomQuery
        )

    def __repr__(self) -> str:
        return f'<Project {self.name}>'
