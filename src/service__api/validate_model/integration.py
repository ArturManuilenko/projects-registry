
from pydantic import BaseModel


class ApiProjectIntegration(BaseModel):
    """Pydantic model"""
    has_confluence: bool
    confluence_url: str
    has_jira: bool
    jira_url: str
    has_gitlab: bool
    gitlab_url: str
    has_trello: bool
    trello_url: str
    has_ips: bool
    ips_url: str
    has_teams: bool
    teams_url: str
    has_enterprise: bool
    enterprise_url: str
    has_kiwi: bool
    kiwi_url: str
