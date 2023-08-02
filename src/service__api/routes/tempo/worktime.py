from typing import Tuple
from flask import request
from flask import Response as FlaskResponse
from src.utils.tempo import TempoException
from src.service__api.utils.response import Response
from src.service__api.main import app, tempo


@app.route('/jira-task/<string:task_key>/worktime', methods=['GET'])
def get_task_worktime(task_key: str) -> Tuple[FlaskResponse, int]:
    from_date = request.args.get('from_date', None)
    to_date = request.args.get('to_date', None)
    try:
        worktime = tempo.get_issue_worklogs(
            issue_id=task_key,
            from_date=from_date,
            to_date=to_date
        )
    except TempoException as e:
        return Response.bad_request_error(e.args[0]).send()

    return Response(payload=worktime).send()


@app.route('/jira-project/<string:project_key>/worktime', methods=['GET'])
def get_project_worktime(project_key: str) -> Tuple[FlaskResponse, int]:
    from_date = request.args.get('from_date', None)
    to_date = request.args.get('to_date', None)
    try:
        worktime = tempo.get_project_worklogs(
            project_key=project_key,
            from_date=from_date,
            to_date=to_date
        )
    except TempoException as e:
        return Response.bad_request_error(e.args[0]).send()

    return Response(payload=worktime).send()


@app.route('/jira-user/<string:user_id>/worktime', methods=['GET'])
def get_user_worktime(user_id: str) -> Tuple[FlaskResponse, int]:
    from_date = request.args.get('from_date', None)
    to_date = request.args.get('to_date', None)
    try:
        worktime = tempo.get_user_worklogs(
            user_id=user_id,
            from_date=from_date,
            to_date=to_date
        )
    except TempoException as e:
        return Response.bad_request_error(e.args[0]).send()

    return Response(payload=worktime).send()
