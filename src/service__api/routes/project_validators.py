from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from api_utils.utils.constants import TJsonResponse
from api_utils.api_resource.api_resource import ApiResource
from api_utils.errors.api_no_result_found import ApiNoResultFoundError

from src.conf.atlassian_api import SERVER
from src.service__api.routes import api_bp
from src.conf.projects_registry__api import api_project_registry
from src.service__api.main import validator, jira
from src.manager__common__db.models.project_release import ProjectRelease
from src.manager__common__db.helpers.project.get_project import get_project_object
from src.manager__common__db.helpers.project_release.get_project_release import get_project_releases


@api_bp.route('/organizations/current/projects/<uuid:project_id>/validations/general', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_project_obj_validations(
    api_resource: ApiResource,
    project_id: UUID
) -> TJsonResponse:
    project_obj = get_project_object(
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    project_validate_result = validator.validate_project(project_obj.to_dict())
    return api_resource.response_list_ok(project_validate_result, len(project_validate_result))


@api_bp.route('/organizations/current/projects/<uuid:project_id>/validations/epics', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_project_epics_validations(api_resource: ApiResource, project_id: UUID) -> TJsonResponse:
    project_obj = get_project_object(
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    project_epics = jira.get_project_epics(project_key=project_obj.key)
    if project_epics is None:
        raise ApiNoResultFoundError(f'project with key "{project_obj.key}" has not epic tasks in Jira')
    project_epics_validate_result = []
    if project_epics is not None:
        for epic in project_epics:
            validate_epic_errors = validator.validate_epic(epic)
            # check if validate_result has errors
            if validate_epic_errors:
                project_epics_validate_result.append({
                    'name': epic.get('name'),
                    'url': SERVER + "/browse/" + epic.get('name'),
                    'validator_results': validator.validate_epic(epic)
                })
    return api_resource.response_list_ok(project_epics_validate_result, len(project_epics_validate_result))


@api_bp.route('/organizations/current/projects/<uuid:project_id>/validations/tasks', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_project_tasks_validations(api_resource: ApiResource, project_id: UUID) -> TJsonResponse:
    project_obj = get_project_object(
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    project_tasks = jira.get_issues(project=project_obj.key)
    if project_tasks is None:
        raise ApiNoResultFoundError(f'project with key "{project_obj.key}" has not tasks in Jira')
    project_tasks_validate_result = []
    if project_tasks is not None:
        for task in project_tasks:
            validate_task_errors = validator.validate_task(task)
            # check if validate_result has errors
            if validate_task_errors:
                project_tasks_validate_result.append({
                    'name': task.get('name'),
                    'url': SERVER + "/browse/" + task.get('name'),
                    'validator_results': validate_task_errors
                })
    return api_resource.response_list_ok(project_tasks_validate_result, len(project_tasks_validate_result))


@api_bp.route('/organizations/current/projects/<uuid:project_id>/validations/bugs', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_project_bugs_validations(api_resource: ApiResource, project_id: UUID) -> TJsonResponse:
    project_obj = get_project_object(
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    project_bugs = jira.get_project_bugs(project_key=project_obj.key)
    if project_bugs is None:
        raise ApiNoResultFoundError(f'project with key "{project_obj.key}" has not bug tasks in Jira')
    project_bugs_validate_result = []
    if project_bugs is not None:
        for bug_task in project_bugs:
            validate_task_errors = validator.validate_bug(bug_task)
            # check if validate_result has errors
            if validate_task_errors:
                project_bugs_validate_result.append({
                    'name': bug_task.get('name'),
                    'url': SERVER + "/browse/" + bug_task.get('name'),
                    'validator_results': validate_task_errors
                })
    return api_resource.response_list_ok(project_bugs_validate_result, len(project_bugs_validate_result))


@api_bp.route('/organizations/current/projects/<uuid:project_id>/validations/stories', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_project_stories_validations(api_resource: ApiResource, project_id: UUID) -> TJsonResponse:
    project_obj = get_project_object(
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    project_stories = jira.get_project_stories(project_key=project_obj.key)
    project_stories_validate_result = []
    if project_stories is None:
        raise ApiNoResultFoundError(f'project with key "{project_obj.key}" has not story tasks in Jira')
    if project_stories is not None:
        for story_task in project_stories:
            validate_task_errors = validator.validate_task(story_task)
            # check if validate_result has errors
            if validate_task_errors:
                project_stories_validate_result.append({
                    'name': story_task.get('name'),
                    'url': SERVER + "/browse/" + story_task.get('name'),
                    'validator_results': validate_task_errors
                })
    return api_resource.response_list_ok(project_stories_validate_result, len(project_stories_validate_result))


@api_bp.route('/organizations/current/projects/<uuid:project_id>/validations/releases', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_project_releases_validations(api_resource: ApiResource, project_id: UUID) -> TJsonResponse:
    project_obj = get_project_object(
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    project_db_releases = get_project_releases(
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    project_jira_releases = jira.get_project_versions(project_obj.key)
    if project_jira_releases is None:
        raise ApiNoResultFoundError(f'project with key "{project_obj.key}" has not releases in Jira')
    project_releases_validate_result = []
    if project_jira_releases is not None:
        for jira_release in project_jira_releases:
            validate_errors: List[Optional[Dict[str, str]]] = validator.validate_releases(jira_release)
            jira_release_in_db: List[ProjectRelease] = [db_release for db_release in project_db_releases if db_release == jira_release.get('name')]
            if jira_release_in_db:
                jira_release_in_db_object: ProjectRelease = jira_release_in_db[0]
                if jira_release.get('name') != jira_release_in_db_object.name:
                    validate_errors.append({
                        'error_type': 'has_correct_name',
                        'error_message': 'jira project release name has not match with project release in system'
                    })
                if jira_release_in_db_object.date_started and datetime.strptime(jira_release.get('start_date'), '%Y-%m-%d').date() != jira_release_in_db_object.date_started.date():
                    validate_errors.append({
                        'error_type': 'has_correct_start_date',
                        'error_message': 'jira project release start date has not match with project release in system '
                    })
                if jira_release_in_db_object.date_finished_real and datetime.strptime(jira_release.get('release_date'), '%Y-%m-%d').date() != jira_release_in_db_object.date_finished_real.date():
                    validate_errors.append({
                        'error_type': 'has_correct_finish_date',
                        'error_message': 'jira project release finish date has not match with project release in system '
                    })
            if validate_errors:
                project_releases_validate_result.append({
                    'name': jira_release.get('name'),
                    'url': SERVER + "/browse/" + jira_release.get('name'),
                    'validator_results': validate_errors
                })
    return api_resource.response_list_ok(project_releases_validate_result, len(project_releases_validate_result))
