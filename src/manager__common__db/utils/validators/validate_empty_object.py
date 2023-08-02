from typing import Any
from db_utils.modules.db import db
from src.manager__common__db.utils.validators.validate_error import ValidateError


def validate_empty_object(obj_id: str, model: db.Model) -> Any:
    obj = model.query.filter_by(id=obj_id).first()
    if not obj:
        raise ValidateError(f'{model.__name__} data was not found')
    return obj
