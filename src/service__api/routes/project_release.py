from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
from db_utils.utils.get_model_template import get_models_template
import src.conf.permissions as permissons
from src.service__api.routes import api_bp
from src.conf.projects_registry__api import api_project_registry
from src.manager__common__db.models.project_release import ProjectRelease
from src.service__api.validate_model.project_release import ApiProjectRelease
from src.manager__common__db.helpers.project_release.add_new_project_release import add_new_project_release
from src.manager__common__db.helpers.project_release.update_project_release import update_project_release
from src.manager__common__db.helpers.project_release.get_project_release import get_project_release_object_query
from src.manager__common__db.helpers.project_release.delete_project_release import delete_project_release


@api_bp.route('/organizations/current/projects/<uuid:project_id>/releases', methods=['POST'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_ADD_ORG_PROJECT_RELEASE)
def pr_add_org_project_release(
        api_resource: ApiResource,
        project_id: UUID,
        body: ApiProjectRelease
) -> TJsonResponse:
    with transaction_commit():
        new_project = add_new_project_release(
            organization_id=api_resource.auth_token.organization_id,
            project_id=project_id,
            name=body.name,
            date_started=body.date_started,
            date_finished_planned=body.date_finished_planned,
            date_finished_real=body.date_finished_real,
            description=body.description,
            conversation_url=body.conversation_url,
            release_scope_url=body.release_scope_url,
            user_created_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_created_ok(new_project.to_dict())


@api_bp.route('/releases/new', methods=['GET'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_GET_PROJECT_RELEASE_TPL)
def pr_get_project_release_tpl(api_resource: ApiResource) -> TJsonResponse:
    project_fields = get_models_template([ProjectRelease])
    return api_resource.response_obj_ok(project_fields)


@api_bp.route('/organizations/current/projects/<uuid:project_id>/releases/<uuid:release_id>', methods=['GET'])
@api_project_registry.rest_api(many=False, access=api_project_registry.ACCESS_PRIVATE)
def api_get_project_release_obj(
    api_resource: ApiResource,
    project_id: UUID,
    release_id: UUID
) -> TJsonResponse:
    project_release_obj = get_project_release_object_query(
        release_id=release_id,
        project_id=project_id,
        organization_id=api_resource.auth_token.organization_id,
        filters=api_resource.filter_by.params,
        sort=api_resource.sort_by.params
    )
    return api_resource.response_obj_ok(project_release_obj.to_dict())


@api_bp.route('/organizations/current/projects/<uuid:project_id>/releases/<uuid:release_id>', methods=['PUT'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_MOD_ORG_PROJECT_RELEASE)
def pr_mod_org_project_release(
    api_resource: ApiResource,
    project_id: UUID,
    release_id: UUID,
    body: ApiProjectRelease
) -> TJsonResponse:
    with transaction_commit():
        project_obj = update_project_release(
            organization_id=api_resource.auth_token.organization_id,
            project_id=project_id,
            release_id=release_id,
            name=body.name,
            date_started=body.date_started,
            date_finished_planned=body.date_finished_planned,
            date_finished_real=body.date_finished_real,
            description=body.description,
            conversation_url=body.conversation_url,
            release_scope_url=body.release_scope_url,
            user_modified_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_ok(project_obj.to_dict())


@api_bp.route('organizations/current/projects/<uuid:project_id>/releases/<uuid:release_id>', methods=['DELETE'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_DELETE_ORG_PROJECT_RELEASE)
def pr_delete_org_project_release(
    api_resource: ApiResource,
    project_id: UUID,
    release_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        delete_project_release(
            project_id=project_id,
            release_id=release_id,
            organization_id=api_resource.auth_token.organization_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()
