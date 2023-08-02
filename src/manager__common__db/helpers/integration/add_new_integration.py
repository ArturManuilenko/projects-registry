from uuid import UUID
from src.manager__common__db.models.integration import Integration
from db_utils.modules.db import db


def add_new_integration(
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
    user_created_id: UUID
) -> Integration:
    integration_object = Integration(
        organization_id=organization_id,
        project_id=project_id,
        has_confluence=has_confluence,
        confluence_url=confluence_url,
        has_jira=has_jira,
        jira_url=jira_url,
        has_gitlab=has_gitlab,
        gitlab_url=gitlab_url,
        has_trello=has_trello,
        trello_url=trello_url,
        has_ips=has_ips,
        ips_url=ips_url,
        has_teams=has_teams,
        teams_url=teams_url,
        has_enterprise=has_enterprise,
        enterprise_url=enterprise_url,
        has_kiwi=has_kiwi,
        kiwi_url=kiwi_url
    )
    integration_object.mark_as_created(user_created_id)
    db.session.add(integration_object)
    return integration_object
