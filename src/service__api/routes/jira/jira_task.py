from src.utils.jira import JiraException
from typing import Tuple
from flask import request
from flask import Response as FlaskResponse
from src.service__api.utils.response import Response
from src.service__api.main import jira
from src.service__api.routes import api_bp as api


@api.route('/jira-task', methods=['GET'])
def get_tasks_list() -> Tuple[FlaskResponse, int]:
    try:
        args = request.args
        offset = int(args.get('offset')) if args.get('offset', None) else None
        limit = int(args.get('limit')) if args.get('limit', None) else None
        payload = jira.get_issues(start=offset, limit=limit)
    except JiraException as e:
        return Response.validation_error(e.args[0]).send()

    return Response(payload=payload).send()


@api.route('/jira-task/<string:task_key>', methods=['GET'])
def task_key(task_key: str) -> Tuple[FlaskResponse, int]:
    try:
        payload = jira.get_issues(key=task_key)
    except JiraException as e:
        return Response.validation_error(e.args[0]).send()

    return Response(payload=payload).send()


@api.route('/jira-project/<string:project_key>/task', methods=['GET'])
def get_project_tasks(project_key: str) -> Tuple[FlaskResponse, int]:
    try:
        project = jira.get_issues(project=project_key)
    except JiraException as e:
        return Response.bad_request_error(e.args[0]).send()

    return Response(payload=project).send()


@api.route('/jira-user/<string:account_id>/task', methods=['GET'])
def get_project_user(account_id: str) -> Tuple[FlaskResponse, int]:
    try:
        project = jira.get_issues(assignee=account_id)
    except JiraException as e:
        return Response.bad_request_error(e.args[0]).send()

    return Response(payload=project).send()


@api.route('/user/<string:account_id>/task/comments', methods=['GET'])
def get_task_comments(account_id: str) -> Tuple[FlaskResponse, int]:
    try:
        task = jira.get_issues(assignee=account_id)
        comment = jira.get_issue_comments(issue_key=task[0]['key'])
    except JiraException as e:
        return Response.bad_request_error(e.args[0]).send()

    return Response(payload=comment).send()
