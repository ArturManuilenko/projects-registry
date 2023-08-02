import os

from api_utils.modules.api_sdk_config import ApiSdkConfig
from api_utils.modules.api_utils_sdk import ApiSdk
from api_utils.utils.decode_base64 import decode_base64_to_string

from src.conf.permissions import permissions

API__VERSION = 'v1'


jwt_public_key = decode_base64_to_string(os.environ['JWT_PUBLIC_KEY'])


api_project_registry = ApiSdk(ApiSdkConfig(
    environment=os.environ['APPLICATION_ENV'],
    permissions=permissions,
    jwt_public_key=jwt_public_key,
    check_access=True,
    debug=False,
))
