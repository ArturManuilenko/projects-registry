from src.utils.jira import JiraException
from typing import Tuple
from flask import Response as FlaskResponse
from src.service__api.utils.response import Response
from src.service__api.main import jira
from src.service__api.routes import api_bp as api


@api.route('/jira-user', methods=['GET'])
def get_user_list() -> Tuple[FlaskResponse, int]:
    try:
        payload = jira.get_all_users()
    except JiraException as e:
        return Response.validation_error(e.args[0]).send()

    return Response(payload=payload).send()


@api.route('/jira-user/<string:account_id>', methods=['GET'])
def get_user_details(account_id: str) -> Tuple[FlaskResponse, int]:
    try:
        project = jira.get_user(account_id=account_id)
    except JiraException as e:
        return Response.bad_request_error(e.args[0]).send()

    return Response(payload=project).send()
