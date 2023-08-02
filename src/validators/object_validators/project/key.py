from src.utils.conflience import ConfluenceException
from src.utils.jira import JiraException
from src.service__api.main import jira, confluence
from src.validators.constants.jira_project import MAX_LENGTH_PROJECT_NAME, MIN_LENGTH_PROJECT_NAME


def project_name_min_length(key: str) -> bool:
    try:
        jira_name = jira.get_project(key=key)['name']
    except JiraException as e:
        raise ValueError(e)
    if jira_name is not None and len(jira_name) > MIN_LENGTH_PROJECT_NAME:
        return True
    else:
        raise ValueError('project name have not correct length in Jira')


def project_name_max_length(key: str) -> bool:
    try:
        jira_name = jira.get_project(key=key)['name']
    except JiraException as e:
        raise ValueError(e)
    if jira_name is not None and len(jira_name) < MAX_LENGTH_PROJECT_NAME:
        return True
    else:
        raise ValueError('project name have not correct length in Jira')


def has_jira(key: str) -> bool:
    if jira.get_project(key=key):
        return True
    raise ValueError(f'project with key "{key}" not found in Jira')


def has_confluence(key: str) -> bool:
    try:
        if confluence.get_project_space(space=key):
            return True
        raise ValueError('project not found in Confluence')
    except ConfluenceException:
        raise ValueError('project not found in Confluence')


def has_gitlab(key: str) -> bool:
    pass


def has_trello(key: str) -> bool:
    pass


def has_kiwi(key: str) -> bool:
    pass


def has_manager(key: str) -> bool:
    project = jira.get_project(key=key)
    if project and project.get('leader', None):
        return True
    raise ValueError('project has not manager in Jira')


def has_type(key: str) -> bool:
    project = jira.get_project(key=key)
    if project and project.get('type', None):
        return True
    raise ValueError('project has not type in Jira')


def has_category(key: str) -> bool:
    project = jira.get_project(key=key)
    if project and project.get('category', None):
        return True
    raise ValueError('project has not category in Jira')


def has_epic(key: str) -> bool:
    epic = jira.get_project_epics(project_key=key)
    if epic:
        return True
    raise ValueError('project has no epic tasks in Jira')


def has_release(key: str) -> bool:
    release = jira.get_project_versions(key=key)
    if release:
        return True
    raise ValueError('project has not release in Jira')


def has_release_dates(key: str) -> bool:
    release = jira.get_project_versions(key=key)
    if release and release.get('start_date', None) and release.get('release_date', None):
        return True
    raise ValueError('project release has not start date or expiration date in Jira')


def has_issues(key: str) -> bool:
    issues = jira.get_issues(project=key)
    if issues:
        return True
    raise ValueError('project has not issues in Jira')


def has_team(key: str) -> bool:
    try:
        teams = jira.get_project_team(project_key=key)
    except JiraException:
        teams = None
    if teams and teams.get('UnicLab Developers', None) and teams.get('UnicLab PM', None):
        return True
    raise ValueError('project has not team in Jira')
