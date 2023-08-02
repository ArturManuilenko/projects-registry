from typing import Any
from uuid import UUID

from src.manager__common__db.utils.validators.validate_error import ValidateError


def validate_uuid4(uuid: Any) -> None:
    try:
        UUID(uuid, version=4)
    except ValueError:
        raise ValidateError('invalid uuid')
