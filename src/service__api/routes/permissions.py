from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from src.service__api.routes import api_bp
from src.conf.projects_registry__api import api_project_registry


@api_bp.route('/permissions', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_permisssions(api_resource: ApiResource) -> TJsonResponse:
    return api_project_registry.get_permisssions_resource()
