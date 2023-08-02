from uuid import UUID
from typing import Optional
from datetime import datetime, timedelta

from src.manager__common__db.utils.category_enum import CategoryProject
from src.manager__common__db.utils.priority_enum import PriorityProject
from src.manager__common__db.utils.type_enum import TypeProject
from src.manager__common__db.utils.validators.validate_error import ValueNotUniqueError
from src.manager__common__db.models.project import Project
from src.manager__common__db.utils.status_enum import StatusProject
from src.manager__common__db.helpers.project.get_project import get_project_object


def update_project(
    name: str,
    key: str,
    project_manager_user_id: UUID,
    date_launched: datetime,
    status: StatusProject,
    is_initiative_document_exists: bool,
    notes: Optional[str],
    type: TypeProject,
    priority: PriorityProject,
    category: CategoryProject,
    customer_organization_id: UUID,
    executor_organization_id: UUID,
    project_id: UUID,
    organization_id: UUID,
    user_modified_id: UUID,
    is_archived: Optional[bool] = False,
) -> Project:
    project = get_project_object(
        organization_id=organization_id,
        project_id=project_id,
        filters=[],
        sort=[]
    )

    # check key unique
    project_duplicate_by_key = Project.query.filter_by(key=key).first()
    if project_duplicate_by_key and project_duplicate_by_key.id != project_id:
        raise ValueNotUniqueError(location='key')

    # check name unique
    project_duplicate_by_name = Project.query.filter_by(name=name).first()
    if project_duplicate_by_name and project_duplicate_by_name.id != project_id:
        raise ValueNotUniqueError(location='name')

    project.name = name
    project.key = key
    project.project_manager_user_id = project_manager_user_id
    project.date_launched = date_launched
    if project.status == status:
        if not is_initiative_document_exists:
            project.status = StatusProject.pending
        elif project.status.value == "PENDING" and is_initiative_document_exists:
            project.status = StatusProject.active
        elif project.status.value == "COMPLETED" and (project.date_launched.replace(tzinfo=None) - project.date_modified.replace(tzinfo=None)) > timedelta(days=60):
            project.status = StatusProject.archived
        elif project.status.value == "ACTIVE" and (project.date_launched.replace(tzinfo=None) - project.date_modified.replace(tzinfo=None)) > timedelta(days=30):
            project.status = StatusProject.completed
    else:
        project.status = status
    project.is_initiative_document_exists = is_initiative_document_exists
    project.is_archived = is_archived
    project.notes = notes
    project.type = type
    project.priority = priority
    project.customer_organization_id = customer_organization_id
    project.executor_organization_id = executor_organization_id
    project.category = category
    project.mark_as_modified(user_modified_id)

    return project
