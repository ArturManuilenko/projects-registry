from api_utils.access import PermissionRegistry


permissions = PermissionRegistry('project_registry', 10100, 11000)


# Project API methods
PERMISSION__PR_GET_PROJECT_TPL = permissions.add('PR_GET_PROJECT_TPL', 1, 'get project template', 'project')
PERMISSION__PR_ADD_ORG_PROJECT = permissions.add('PR_ADD_ORG_PROJECT', 4, 'create new organization project', 'project')
PERMISSION__PR_MOD_ORG_PROJECT = permissions.add('PR_MOD_ORG_PROJECT', 5, 'update organization project', 'project')

# Project releases API methods
PERMISSION__PR_GET_PROJECT_RELEASE_TPL = permissions.add('PR_GET_PROJECT_RELEASE_TPL', 6, 'get project release template', 'project_release')
PERMISSION__PR_ADD_ORG_PROJECT_RELEASE = permissions.add('PR_ADD_ORG_PROJECT_RELEASE', 8, 'create new organization project release', 'project_release')
PERMISSION__PR_MOD_ORG_PROJECT_RELEASE = permissions.add('PR_MOD_ORG_PROJECT_RELEASE', 9, 'update organization project release', 'project_release')
PERMISSION__PR_DELETE_ORG_PROJECT_RELEASE = permissions.add('PR_DELETE_ORG_PROJECT_RELEASE', 10, 'delete organization project release', 'project_release')

# Project modifications API methods
PERMISSION__PR_ADD_ORG_PROJECT_MODIFICATION = permissions.add('PR_ADD_ORG_PROJECT_MODIFICATION', 14, 'add organization project modification', 'project_modifications')
PERMISSION__PR_MOD_ORG_PROJECT_MODIFICATION = permissions.add('PR_MOD_ORG_PROJECT_MODIFICATION', 15, 'update organization project modification', 'project_modifications')
PERMISSION__PR_DELETE_ORG_PROJECT_MODIFICATION = permissions.add('PR_DELETE_ORG_PROJECT_MODIFICATION', 16, 'delete organization project modification', 'project_modifications')

# Project integration API methods
PERMISSION__PR_MOD_ORG_PROJECT_INTEGRATION = permissions.add('PR_MOD_ORG_PROJECT_INTEGRATION', 17, 'update organization project integration', 'project_integration')
