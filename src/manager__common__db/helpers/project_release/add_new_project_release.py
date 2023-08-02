from uuid import UUID
from datetime import datetime, timedelta

from db_utils.modules.db import db
from src.manager__common__db.models.project_release import ProjectRelease
from src.manager__common__db.utils.project_release_stasus import StatusRelease


def add_new_project_release(
    organization_id: UUID,
    project_id: UUID,
    name: str,
    date_started: datetime,
    date_finished_planned: datetime,
    date_finished_real: datetime,
    description: str,
    conversation_url: str,
    release_scope_url: str,
    user_created_id: UUID
) -> ProjectRelease:
    new_project_release = ProjectRelease(
        organization_id=organization_id,
        project_id=project_id,
        name=name,
        date_started=date_started,
        date_finished_planned=date_finished_planned,
        date_finished_real=date_finished_real,
        description=description,
        conversation_url=conversation_url,
        release_scope_url=release_scope_url,
    )

    if not date_finished_real:
        new_project_release.status = StatusRelease.success
        # now = datetime.now()
        # if new_project_release.date_finished_planned.replace(tzinfo=None) >= now.replace(tzinfo=None):
        #     new_project_release.status = StatusRelease.success
        # elif (now.replace(tzinfo=None) - new_project_release.date_finished_planned.replace(tzinfo=None)).days <= timedelta(days=30).days:
        #     new_project_release.status = StatusRelease.late
        # elif (now.replace(tzinfo=None) - new_project_release.date_finished_planned.replace(tzinfo=None)).days > timedelta(days=30).days:
        #     new_project_release.status = StatusRelease.missed
    else:
        if new_project_release.date_finished_real.replace(tzinfo=None) == new_project_release.date_finished_planned.replace(tzinfo=None):
            new_project_release.status = StatusRelease.success
        elif (new_project_release.date_finished_real.replace(tzinfo=None) - new_project_release.date_finished_planned.replace(tzinfo=None)).days <= timedelta(days=30).days:
            new_project_release.status = StatusRelease.late
        elif (new_project_release.date_finished_real.replace(tzinfo=None) - new_project_release.date_finished_planned.replace(tzinfo=None)).days > timedelta(days=30).days:
            new_project_release.status = StatusRelease.missed

    new_project_release.mark_as_created(user_created_id=user_created_id)
    db.session.add(new_project_release)
    return new_project_release
