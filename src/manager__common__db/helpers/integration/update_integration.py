from uuid import UUID
from sqlalchemy import and_
from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.manager__common__db.models.integration import Integration


def update_integration(
    integration_id: UUID,
    organization_id: UUID,
    project_id: UUID,
    has_confluence: bool,
    confluence_url: str,
    has_jira: bool,
    jira_url: str,
    has_gitlab: bool,
    gitlab_url: str,
    has_trello: bool,
    trello_url: str,
    has_ips: bool,
    ips_url: str,
    has_teams: bool,
    teams_url: str,
    has_enterprise: bool,
    enterprise_url: str,
    has_kiwi: bool,
    kiwi_url: str,
    user_modified_id: UUID
) -> Integration:
    integration_obj = Integration.query.with_deleted().filter(
        and_(
            Integration.organization_id == organization_id,
            Integration.project_id == project_id,
            Integration.id == integration_id
        )).first()

    enshure_db_object_exists(Integration, integration_obj)

    integration_obj.has_confluence = has_confluence
    integration_obj.confluence_url = confluence_url
    integration_obj.has_jira = has_jira
    integration_obj.jira_url = jira_url
    integration_obj.has_gitlab = has_gitlab
    integration_obj.gitlab_url = gitlab_url
    integration_obj.has_trello = has_trello
    integration_obj.trello_url = trello_url
    integration_obj.has_ips = has_ips
    integration_obj.ips_url = ips_url
    integration_obj.has_teams = has_teams
    integration_obj.teams_url = teams_url
    integration_obj.has_enterprise = has_enterprise
    integration_obj.enterprise_url = enterprise_url
    integration_obj.has_kiwi = has_kiwi
    integration_obj.kiwi_url = kiwi_url

    integration_obj.mark_as_modified(user_modified_id)

    return integration_obj
