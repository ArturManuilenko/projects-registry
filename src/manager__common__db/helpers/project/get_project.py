from db_utils.modules.db import db
from src.manager__common__db.utils.filtering.search import db_search    # type: ignore
from typing import Any, Dict, List, Tuple
from uuid import UUID
from src.manager__common__db.models.project import Project
from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists


def get_project_list(
    organization_id: UUID,
    filters: List[Dict[str, Any]],
    sort: List[Tuple[str, str]],
    limit: int,
    offset: int
) -> List[Project]:
    filters.append(
        {
            "name": "organization_id",
            "op": "==",
            "val": organization_id,
        }
    )
    sort.append(('+', 'status'))
    sort.append(('+', 'priority'))
    project_list = db_search(
        session=db,
        model=Project,
        filters=filters,
        sort=sort,
    ).offset(offset).limit(limit).all()
    return project_list


def get_project_object(
    organization_id: UUID,
    project_id: UUID,
    filters: List[Dict[str, Any]],
    sort: List[Tuple[str, str]]
) -> Project:
    filters.append(
        {
            "and": [
                {
                    "name": "id",
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
    project = db_search(
        session=db,
        model=Project,
        filters=filters,
        sort=sort,
    ).first()
    return enshure_db_object_exists(Project, project)


def get_project_list_total_count(organization_id: UUID) -> int:
    return Project.query.filter_by(organization_id=organization_id).count()
