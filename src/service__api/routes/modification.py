from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
import src.conf.permissions as permissons
from src.service__api.routes import api_bp
from src.conf.projects_registry__api import api_project_registry
from src.manager__common__db.helpers.modification.update_modification import update_modification
from src.manager__common__db.helpers.modification.add_new_modification import add_new_modification
from src.manager__common__db.helpers.modification.delete_modification import delete_modification
from src.service__api.validate_model.modification import ApiProjectModification


@api_bp.route('/organizations/current/projects/<uuid:project_id>/modifications/<uuid:mod_id>', methods=['PUT'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_MOD_ORG_PROJECT_MODIFICATION)
def pr_mod_org_project_modification(
    api_resource: ApiResource,
    body: ApiProjectModification,
    project_id: UUID,
    mod_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        modification_obj = update_modification(
            name=body.name,
            project_id=project_id,
            modification_id=mod_id,
            organization_id=api_resource.auth_token.organization_id,
            user_modified_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_ok(modification_obj.to_dict())


@api_bp.route('/organizations/current/projects/<uuid:project_id>/modifications', methods=['POST'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_ADD_ORG_PROJECT_MODIFICATION)
def pr_add_org_project_modification(
    api_resource: ApiResource,
    body: ApiProjectModification,
    project_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        modification_obj = add_new_modification(
            name=body.name,
            project_id=project_id,
            organization_id=api_resource.auth_token.organization_id,
            user_created_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_ok(modification_obj.to_dict())


@api_bp.route('/organizations/current/projects/<uuid:project_id>/modifications/<uuid:modification_id>', methods=['DELETE'])
@api_project_registry.rest_api(many=False, access=permissons.PERMISSION__PR_DELETE_ORG_PROJECT_MODIFICATION)
def pr_delete_org_project_modification(
    api_resource: ApiResource,
    project_id: UUID,
    modification_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        delete_modification(
            modification_id=modification_id,
            project_id=project_id,
            organization_id=api_resource.auth_token.organization_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()
