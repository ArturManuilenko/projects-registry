from uuid import UUID
from sqlalchemy import and_
from src.manager__common__db.models.project_release import ProjectRelease


def delete_project_release(
    organization_id: UUID,
    release_id: UUID,
    project_id: UUID,
    user_deleted_id: UUID
) -> None:
    project_release_obj = ProjectRelease.query.filter(
        and_(
            ProjectRelease.id == release_id,
            ProjectRelease.project_id == project_id,
            ProjectRelease.organization_id == organization_id
        )
    ).first()
    if project_release_obj is not None:
        project_release_obj.mark_as_deleted(user_deleted_id)
