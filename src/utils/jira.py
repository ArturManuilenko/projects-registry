from typing import Dict, List, Optional, Any
from requests import HTTPError
from src.vendor.atlassian import Jira as VendorJira
from src.utils.formatting import custom_time
import src.conf.atlassian_api as atlassian_conf
from src.utils.cache import cache_result


class JiraException(HTTPError):
    pass


class Jira():
    __client = None

    def __init__(self) -> None:
        try:
            self.__client = VendorJira(
                url=atlassian_conf.SERVER,
                username=atlassian_conf.USERNAME,
                password=atlassian_conf.TOKEN,
                cloud=True
            )
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))

    @cache_result
    def get_project_versions(self, key: str) -> List[Dict[str, Any]]:

        try:
            project_versions = self.__client.get_project_versions(key, expand='startDate')
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))

        versions = []
        for version in project_versions:
            versions.append({
                'jira_id': version.get('id', None),
                'name': version.get('name', None),
                'description': version.get('description', None),
                'start_date': version.get('startDate', None),
                'release_date': version.get('releaseDate', None),
                'is_released': version.get('released', None),
                'user_released_date': version.get('userReleaseDate', None),
                'is_archived': version.get('archived', None)
            })
        return versions

    @cache_result
    def get_project(self, key: str) -> Dict[str, Any]:
        try:
            project = self.__client.get_project(key, expand='categoryId')
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))
        return {
            'key': project.get('key', None),
            'name': project.get('name', None),
            'description': project.get('description', None),
            'type': project.get('projectTypeKey', None),
            'category': {
                'name': project['projectCategory'].get('name'),
                'description': project['projectCategory'].get('description')
            } if project.get('projectCategory', None) else None,
            'leader': {
                'jira_id': project.get('lead', None).get('accountId', None),
                'name': project.get('lead', None).get('displayName', None)
            } if project.get('lead', None) else None
        } if project else None

    @cache_result
    def get_all_users(self) -> List[Dict[str, Any]]:

        try:
            users = self.__client.get_all_users()
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))
        people_users = [user for user in users if user.get('accountType', '') != 'app']
        return [{
            'jira_id': user.get('accountId'),
            'name': user.get('displayName'),
            'email': user.get('emailAddress')
        } for user in people_users]

    @cache_result
    def get_user(self, account_id: str) -> Dict[str, Any]:

        try:
            user = self.__client.user(account_id=account_id)
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))

        return {
            'jira_id': user.get('accountId'),
            'name': user.get('displayName'),
            'email': user.get('emailAddress')
        } if user else None

    @cache_result
    def get_sprint(self, sprint_id: int) -> Dict[str, Any]:

        try:
            sprint = self.__client.sprint(id=sprint_id)
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))

        return {
            'jira_id': sprint.get('id', None),
            'name': sprint.get('name', None),
            'goal': sprint.get('goal', None),
            'start_date': sprint.get('isoStartDate', None),
            'end_date': sprint.get('isoEndDate', None)
        } if sprint else None

    @cache_result
    def get_projects(self) -> List[Dict[str, Any]]:
        projects_result = []
        try:
            projects = self.__client.get_all_projects()
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))
        for project in projects:
            projects_result.append({
                'key': project.get('key', None),
                'name': project.get('name', None),
                'type': project.get('projectTypeKey', None),
                'category': {
                    'name': project['projectCategory'].get('name'),
                    'description': project['projectCategory'].get('description')
                } if project.get('projectCategory', None) else None
            })
        return projects_result

    @cache_result
    def get_issues(
        self,
        start: Optional[int] = 0,
        limit: Optional[int] = 100,
        current_sprint: bool = True,
        **kwargs: Optional[str]
    ) -> List[Dict[str, Any]]:
        """
        Avaliable serach parametrs:
        accountId
        project (key)
        """
        issues_result = []
        searchstring = ' and '.join([(_ + "=" + str(kwargs[_])) if _ != 'condition' else kwargs[_] for _ in kwargs])
        if current_sprint:
            searchstring += ' and Sprint in openSprints()'
        try:
            issues = self.__client.jql(searchstring, start=start, limit=limit)
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))

        for issue in issues['issues']:
            fields = issue.get('fields')
            issues_result.append({
                'name': issue.get('key', None),
                'summary': fields.get('summary', None),
                'description': fields.get('description', None),
                'version': [version.get('name') for version in fields['fixVersions']] if fields.get('fixVersions', None) else None,
                'user_creator_id': fields['reporter'].get('accountId') if fields.get('reporter', None) else None,
                'user_assignee_id': fields['assignee'].get('accountId') if fields.get('assignee', None) else None,
                'issue_type': fields['issuetype'].get('name') if fields.get('issuetype', None) else None,
                'story_points': fields.get('customfield_11916', None),
                'time_original_estimate': custom_time(fields.get('timeoriginalestimate', None)),
                'time_remaining': custom_time(fields.get('timeestimate', None)),
                'time_spent': custom_time(fields.get('timespent', None)),
                'created_date': fields.get('created', None),
                'components': [component.get('name') for component in fields['components']] if fields.get('components', None) else None,
                'resolution_date': fields.get('resolutiondate', None),
                'status': fields['status'].get('name') if fields.get('status', None) else None,
                'progress': str(fields['progress'].get('percent', None)) + '%' if fields.get('progress', None) else None,
                'priority': fields['priority'].get('name') if fields.get('priority', None) else None,
                'difficult': fields.get('customfield_11100', None),
                'sprint': {
                    "jira_id": fields['customfield_10004'][0].get('id', None),
                    "name": fields['customfield_10004'][0].get('name', None),
                    "goal": fields['customfield_10004'][0].get('goal', None),
                    "start_date": fields['customfield_10004'][0].get('startDate', None),
                    "end_date": fields['customfield_10004'][0].get('endDate', None)
                } if fields.get('customfield_10004', None) else None,
                'subtasks': [task.get('name') for task in fields['subtasks']] if fields.get('subtasks', None) else None,
                'epic_link': atlassian_conf.SERVER + "/browse/" + fields['customfield_10006'] if fields.get('customfield_10006', None) else None,
                'business_needs': fields.get('customfield_11931', None),
                'expected_result': fields.get('customfield_10509', None),
                'modifications': fields.get('labels')
            })
        return issues_result

    @cache_result
    def get_project_epics(self, project_key: str) -> List[Dict[str, Any]]:
        try:
            epics = self.get_issues(project=project_key, current_sprint=False, issuetype='Epic')
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))
        return epics if epics else None

    @cache_result
    def get_project_stories(self, project_key: str) -> List[Dict[str, Any]]:
        try:
            stories = self.get_issues(project=project_key, current_sprint=False, issuetype='Story')
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))
        return stories if stories else None

    @cache_result
    def get_project_bugs(self, project_key: str) -> List[Dict[str, Any]]:
        try:
            bugs = self.get_issues(project=project_key, current_sprint=False, issuetype='Bug')
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))
        return bugs if bugs else None

    @cache_result
    def get_issue_comments(self, issue_key: str = None) -> List[Dict[str, Any]]:
        try:
            comments = self.__client.get_issue_comments(issue_key=issue_key)
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))

        return [comment.body for comment in comments] if comments else None

    @cache_result
    def get_project_team(self, project_key: str = None) -> Dict[str, Any]:
        try:
            project_teams = {}
            project_roles = self.__client.get_project_roles(project_key=project_key)
            for role_name, url in project_roles.items():
                role_actors = self.__client.get_project_actors_for_role_project(project_key, url.split('/')[-1])
                role_actors = [actor.get('displayName') for actor in role_actors if actor.get('type') == 'atlassian-user-role-actor']
                project_teams.update({role_name: role_actors})
        except HTTPError as e:
            raise JiraException(*e.response.json().get('errorMessages', None))
        return project_teams if project_teams else None
