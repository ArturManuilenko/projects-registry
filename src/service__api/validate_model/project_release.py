from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator
from src.manager__common__db.utils.validators.validate_error import ValueLengthError


class ApiProjectRelease(BaseModel):
    """Pydantic model"""
    name: str
    date_started: datetime = datetime.utcnow()
    date_finished_planned: datetime
    date_finished_real: Optional[datetime] = ...        # type: ignore
    description: Optional[str] = ...                    # type: ignore
    conversation_url: Optional[str] = ...               # type: ignore
    release_scope_url: Optional[str] = ...              # type: ignore

    @validator('name', allow_reuse=True)
    def check_name_length(cls, value: str) -> str:  # noqa
        if value and not 0 < len(value) < 255:
            raise ValueLengthError(min=0, max=255, get=len(value))
        return value

    @validator('description', allow_reuse=True)
    def check_description_length(cls, value: str) -> str:  # noqa
        if value and not 0 < len(value) < 2000:
            raise ValueLengthError(min=0, max=2000, get=len(value))
        return value

    @validator('conversation_url', allow_reuse=True)
    def check_conversation_url_length(cls, value: str) -> str:  # noqa
        if value and not 0 < len(value) < 1000:
            raise ValueLengthError(min=0, max=1000, get=len(value))
        return value

    @validator('release_scope_url', allow_reuse=True)
    def check_release_scope_url_length(cls, value: str) -> str:  # noqa
        if value and not 0 < len(value) < 1000:
            raise ValueLengthError(min=0, max=1000, get=len(value))
        return value
