from uuid import UUID
from typing import Any, Dict, List, Tuple
from db_utils.modules.db import db
from db_utils.modules.custom_query import CustomQuery
from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.manager__common__db.utils.filtering.search import db_search            # type: ignore
from src.manager__common__db.models.project_release import ProjectRelease


def get_project_release_object_query(
    release_id: UUID,
    project_id: UUID,
    organization_id: UUID,
    filters: List[Dict[str, Any]],
    sort: List[Tuple[str, int]]
) -> ProjectRelease:
    filters.append(
        {
            "and": [
                {
                    "name": "id",
                    "op": "==",
                    "val": release_id,
                },
                {
                    "name": "project_id",
                    "op": "==",
                    "val": project_id,
                },
                {
                    "name": "organization_id",
                    "op": "==",
                    "val": organization_id,
                },
            ]
        }
    )
    project_release = db_search(
        session=db,
        model=ProjectRelease,
        filters=filters,
        sort=sort,
        _initial_query=CustomQuery
    ).first()
    return enshure_db_object_exists(ProjectRelease, project_release)


def get_project_releases(
    project_id: UUID,
    organization_id: UUID,
    filters: List[Dict[str, Any]],
    sort: List[Tuple[str, int]]
) -> List[ProjectRelease]:
    filters.append(
        {
            "and": [
                {
                    "name": "project_id",
                    "op": "==",
                    "val": project_id,
                },
                {
                    "name": "organization_id",
                    "op": "==",
                    "val": organization_id,
                },
            ]
        }
    )
    project_release = db_search(
        session=db,
        model=ProjectRelease,
        filters=filters,
        sort=sort,
        _initial_query=CustomQuery
    ).first()
    return project_release
