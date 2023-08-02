from src.utils.jira import JiraException
from typing import Tuple
from flask import Response as FlaskResponse
from src.service__api.utils.response import Response
from src.service__api.main import jira
from src.service__api.routes import api_bp as api


@api.route('/jira-project', methods=['GET'])
def get_project_list() -> Tuple[FlaskResponse, int]:
    try:
        payload = jira.get_projects()
    except JiraException as e:
        return Response.validation_error(e.args[0]).send()

    return Response(payload=payload).send()


@api.route('/jira-project/<string:project_key>', methods=['GET'])
def get_project_details(project_key: str) -> Tuple[FlaskResponse, int]:
    try:
        project = jira.get_project(key=project_key)
    except JiraException as e:
        return Response.bad_request_error(e.args[0]).send()

    return Response(payload=project).send()
