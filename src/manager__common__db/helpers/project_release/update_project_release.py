from uuid import UUID
from datetime import datetime, timedelta

from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.manager__common__db.models.project_release import ProjectRelease
from src.manager__common__db.utils.project_release_stasus import StatusRelease


def update_project_release(
    release_id: UUID,
    organization_id: UUID,
    project_id: UUID,
    name: str,
    date_started: datetime,
    date_finished_planned: datetime,
    date_finished_real: datetime,
    description: str,
    conversation_url: str,
    release_scope_url: str,
    user_modified_id: UUID
) -> ProjectRelease:
    project_release = ProjectRelease.query.filter_by(
        id=release_id,
        project_id=project_id,
        organization_id=organization_id
    ).first()

    enshure_db_object_exists(ProjectRelease, project_release)

    project_release.name = name
    project_release.date_started = date_started
    project_release.date_finished_planned = date_finished_planned
    project_release.date_finished_real = date_finished_real
    project_release.description = description
    project_release.conversation_url = conversation_url
    project_release.release_scope_url = release_scope_url

    if not project_release.date_finished_real:
        project_release.status = StatusRelease.success
        # now = datetime.now()
        # if project_release.date_finished_planned.replace(tzinfo=None) >= now.replace(tzinfo=None):
        # elif (now.replace(tzinfo=None) - project_release.date_finished_planned.replace(tzinfo=None)).days <= timedelta(days=30).days:
        #     project_release.status = StatusRelease.late
        # elif (now.replace(tzinfo=None) - project_release.date_finished_planned.replace(tzinfo=None)).days > timedelta(days=30).days:
        #     project_release.status = StatusRelease.missed
    else:
        if project_release.date_finished_real.replace(tzinfo=None) <= project_release.date_finished_planned.replace(tzinfo=None):
            project_release.status = StatusRelease.success
        elif (project_release.date_finished_real.replace(tzinfo=None) - project_release.date_finished_planned.replace(tzinfo=None)).days <= timedelta(days=30).days:
            project_release.status = StatusRelease.late
        elif (project_release.date_finished_real.replace(tzinfo=None) - project_release.date_finished_planned.replace(tzinfo=None)).days > timedelta(days=30).days:
            project_release.status = StatusRelease.missed

    project_release.mark_as_modified(user_modified_id)

    return project_release
