from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
from db_utils.utils.get_model_template import get_models_template
import src.conf.permissions as permissons
from src.conf.projects_registry__api import api_project_registry
from src.service__api.validate_model.project import ApiProject
from src.manager__common__db.models.modification import Modification
from src.manager__common__db.models.integration import Integration
from src.manager__common__db.models.project import Project
from src.manager__common__db.helpers.project.get_project import get_project_list, \
    get_project_list_total_count, get_project_object
from src.manager__common__db.helpers.project.add_new_project import add_new_project
from src.manager__common__db.helpers.project.update_project import update_project
from src.service__api.routes import api_bp


@api_bp.route('/projects/new', methods=['GET'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_GET_PROJECT_TPL)
def pr_get_project_tpl(api_resource: ApiResource) -> TJsonResponse:
    project_fields = get_models_template([Project])
    project_fields.update({'modifications': get_models_template([Modification])})
    project_fields.update({'integration': get_models_template([Integration])})
    return api_resource.response_obj_ok(project_fields)


@api_bp.route('/organizations/current/projects', methods=['GET'])
@api_project_registry.rest_api(many=True, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_projects_list(api_resource: ApiResource) -> TJsonResponse:
    project_list = get_project_list(
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_project_list_total_count(api_resource.auth_token.organization_id)
    projects = [project.to_dict() for project in project_list]
    return api_resource.response_list_ok(projects, total_count)


@api_bp.route('/organizations/current/projects/<uuid:project_id>', methods=['GET'])
@api_project_registry.rest_api(many=False, access=api_project_registry.ACCESS_PRIVATE)
def pr_get_project(api_resource: ApiResource, project_id: UUID) -> TJsonResponse:
    project_obj = get_project_object(
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    return api_resource.response_obj_ok(project_obj.to_dict())


@api_bp.route('/organizations/current/projects', methods=['POST'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_ADD_ORG_PROJECT)
def pr_add_org_project(
    api_resource: ApiResource,
    body: ApiProject
) -> TJsonResponse:
    with transaction_commit():
        new_project = add_new_project(
            organization_id=api_resource.auth_token.organization_id,
            name=body.name,
            key=body.key,
            project_manager_user_id=body.project_manager_user_id,
            date_launched=body.date_launched,
            status=body.status,
            is_initiative_document_exists=body.is_initiative_document_exists,
            is_archived=body.is_archived,
            notes=body.notes,
            project_type=body.type,
            priority=body.priority,
            category=body.category,
            customer_organization_id=body.customer_organization_id,
            executor_organization_id=body.executor_organization_id,
            modifications=body.modifications,
            integration=body.integration,
            user_created_id=api_resource.auth_token.user_id,
        )
    return api_resource.response_obj_created_ok(new_project.to_dict())


@api_bp.route('/organizations/current/projects/<uuid:project_id>', methods=['PUT'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_MOD_ORG_PROJECT)
def pr_mod_org_project(
    api_resource: ApiResource,
    project_id: UUID,
    body: ApiProject
) -> TJsonResponse:
    with transaction_commit():
        project_obj = update_project(
            organization_id=api_resource.auth_token.organization_id,
            project_id=project_id,
            name=body.name,
            key=body.key,
            project_manager_user_id=body.project_manager_user_id,
            date_launched=body.date_launched,
            status=body.status,
            is_initiative_document_exists=body.is_initiative_document_exists,
            is_archived=body.is_archived,
            notes=body.notes,
            type=body.type,
            priority=body.priority,
            category=body.category,
            customer_organization_id=body.customer_organization_id,
            executor_organization_id=body.executor_organization_id,
            user_modified_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_ok(project_obj.to_dict())
