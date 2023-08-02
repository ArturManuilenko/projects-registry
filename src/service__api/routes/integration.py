from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
import src.conf.permissions as permissions
from src.conf.projects_registry__api import api_project_registry
from src.manager__common__db.helpers.integration.update_integration import update_integration
from src.service__api.validate_model.integration import ApiProjectIntegration
from src.service__api.routes import api_bp


@api_bp.route('/organizations/current/projects/<uuid:project_id>/integrations/<uuid:integration_id>', methods=['PUT'])
@api_project_registry.rest_api(many=False, access=permissions.PERMISSION__PR_MOD_ORG_PROJECT_INTEGRATION)
def pr_mod_org_project_integration(
    api_resource: ApiResource,
    body: ApiProjectIntegration,
    project_id: UUID,
    integration_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        integration_obj = update_integration(
            integration_id=integration_id,
            organization_id=api_resource.auth_token.organization_id,
            project_id=project_id,
            has_confluence=body.has_confluence,
            confluence_url=body.confluence_url,
            has_jira=body.has_jira,
            jira_url=body.jira_url,
            has_gitlab=body.has_gitlab,
            gitlab_url=body.gitlab_url,
            has_trello=body.has_trello,
            trello_url=body.trello_url,
            has_ips=body.has_ips,
            ips_url=body.ips_url,
            has_teams=body.has_teams,
            teams_url=body.teams_url,
            has_enterprise=body.has_enterprise,
            enterprise_url=body.enterprise_url,
            has_kiwi=body.has_kiwi,
            kiwi_url=body.kiwi_url,
            user_modified_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_ok(integration_obj.to_dict())
