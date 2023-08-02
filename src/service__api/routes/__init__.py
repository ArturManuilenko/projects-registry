from flask import Blueprint

api_bp = Blueprint('api', __name__)

from src.service__api.routes.jira import jira_project    # noqa: E402
from src.service__api.routes.jira import jira_task       # noqa: E402
from src.service__api.routes.jira import jira_user       # noqa: E402
from src.service__api.routes.tempo import worktime       # noqa: E402
from src.service__api.routes import base_exceptions      # noqa: E402
from src.service__api.routes import project_category     # noqa: E402
from src.service__api.routes import project_statuses     # noqa: E402
from src.service__api.routes import project_types        # noqa: E402
from src.service__api.routes import project_priorities   # noqa: E402
from src.service__api.routes import project_release      # noqa: E402
from src.service__api.routes import project_validators   # noqa: E402
from src.service__api.routes import project              # noqa: E402
from src.service__api.routes import modification         # noqa: E402
from src.service__api.routes import integration          # noqa: E402
from src.service__api.routes import permissions          # noqa: E402


__all__ = (
    'base_exceptions',
    'jira_project',
    'jira_task',
    'jira_user',
    'worktime',
    'project',
    'worktime',
    'project_category',
    'project_statuses',
    'project_priorities',
    'project_types',
    'modification',
    'integration',
    'project_release',
    'project_validators',
    'permissions'
)
