from datetime import datetime

from typing import Optional, List
from pydantic import BaseModel, validator
from pydantic.types import UUID4
from src.service__api.validate_model.modification import ApiProjectModification
from src.service__api.validate_model.integration import ApiProjectIntegration
from src.manager__common__db.utils.type_enum import TypeProject
from src.manager__common__db.utils.status_enum import StatusProject
from src.manager__common__db.utils.priority_enum import PriorityProject
from src.manager__common__db.utils.category_enum import CategoryProject
from src.manager__common__db.utils.validators.validate_error import ValueLengthError


class ApiProject(BaseModel):
    """Pydantic model"""
    name: str
    key: str
    project_manager_user_id: UUID4
    date_launched: datetime
    status: StatusProject
    is_initiative_document_exists: bool
    is_archived: Optional[bool] = False
    notes: Optional[str]
    type: TypeProject
    priority: PriorityProject
    category: CategoryProject
    customer_organization_id: UUID4
    executor_organization_id: UUID4
    modifications: List[ApiProjectModification]
    integration: ApiProjectIntegration

    @validator('key', allow_reuse=True)
    def check_key_length(cls, value: str) -> str:  # noqa
        if not 0 < len(value) < 5:
            raise ValueLengthError(min=0, max=5, get=len(value))
        return value
