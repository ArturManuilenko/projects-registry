from typing import Any
from pydantic import PydanticValueError
from src.manager__common__db.utils.constants import TKwargs


class ValidateError(Exception):
    def __init__(self, message: str, *args: Any, **kwargs: TKwargs):
        super().__init__(*args, **kwargs)  # type: ignore
        self.message = message


class ValueNotUniqueError(PydanticValueError):
    code = "not_uniq"
    location = ["{location}"]
    msg_template = 'value is not unique'


class ValueNotAvailableError(PydanticValueError):
    code = "not_avalible"
    location = ["{location}"]
    msg_template = 'value not available'


class ValueLengthError(PydanticValueError):
    code = "length"
    location = ["{location}"]
    msg_template = 'lentgh must be more then {min} and less then {max} symbols, get {get}'
