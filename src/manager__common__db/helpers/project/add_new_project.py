from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime

from db_utils.modules.db import db
from src.manager__common__db.helpers.integration.add_new_integration import add_new_integration
from src.manager__common__db.helpers.modification.add_new_modification import add_new_modification
from src.service__api.validate_model.integration import ApiProjectIntegration
from src.service__api.validate_model.modification import ApiProjectModification
from src.manager__common__db.utils.category_enum import CategoryProject
from src.manager__common__db.utils.priority_enum import PriorityProject
from src.manager__common__db.utils.type_enum import TypeProject
from src.manager__common__db.utils.status_enum import StatusProject
from src.manager__common__db.models.project import Project
from src.manager__common__db.utils.validators.validate_error import ValueNotUniqueError


def add_new_project(
    name: str,
    key: str,
    project_manager_user_id: UUID,
    date_launched: datetime,
    status: StatusProject,
    is_initiative_document_exists: bool,
    notes: Optional[str],
    project_type: TypeProject,
    priority: PriorityProject,
    category: CategoryProject,
    organization_id: UUID,
    customer_organization_id: UUID,
    executor_organization_id: UUID,
    modifications: List[ApiProjectModification],
    integration: ApiProjectIntegration,
    user_created_id: UUID,
    is_archived: Optional[bool] = False,
) -> Project:
    # check key unique
    project_duplicate_by_key = Project.query.filter_by(key=key).first()
    if project_duplicate_by_key:
        raise ValueNotUniqueError(location='key')

    # check name unique
    project_duplicate_by_name = Project.query.filter_by(name=name).first()
    if project_duplicate_by_name:
        raise ValueNotUniqueError(location='name')

    new_project = Project(
        id=uuid4(),
        organization_id=organization_id,
        name=name,
        key=key,
        project_manager_user_id=project_manager_user_id,
        date_launched=date_launched,
        status=status,
        is_initiative_document_exists=is_initiative_document_exists,
        is_archived=is_archived,
        notes=notes,
        type=project_type,
        priority=priority,
        category=category,
        customer_organization_id=customer_organization_id,
        executor_organization_id=executor_organization_id,
    )
    new_project.mark_as_created(user_created_id)
    db.session.add(new_project)

    for modification in modifications:
        add_new_modification(
            organization_id=organization_id,
            project_id=new_project.id,
            name=modification.name,
            user_created_id=user_created_id
        )

    if integration:
        add_new_integration(
            organization_id=organization_id,
            project_id=new_project.id,
            has_confluence=integration.has_confluence,
            confluence_url=integration.confluence_url,
            has_jira=integration.has_jira,
            jira_url=integration.jira_url,
            has_gitlab=integration.has_gitlab,
            gitlab_url=integration.gitlab_url,
            has_trello=integration.has_trello,
            trello_url=integration.trello_url,
            has_ips=integration.has_ips,
            ips_url=integration.ips_url,
            has_teams=integration.has_teams,
            teams_url=integration.teams_url,
            has_enterprise=integration.has_enterprise,
            enterprise_url=integration.enterprise_url,
            has_kiwi=integration.has_kiwi,
            kiwi_url=integration.kiwi_url,
            user_created_id=user_created_id
        )
    return new_project
