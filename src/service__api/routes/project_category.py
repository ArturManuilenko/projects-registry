from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from src.conf.projects_registry__api import api_project_registry
from src.manager__common__db.utils.category_enum import CategoryProject
from src.manager__common__db.helpers.get_enum_fields import get_enum_fields
from src.service__api.routes import api_bp


@api_bp.route('/project-categories', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_project_category_list(api_resource: ApiResource) -> TJsonResponse:
    project_categories = get_enum_fields(CategoryProject)
    return api_resource.response_list_ok(project_categories, total_count=len(project_categories))
