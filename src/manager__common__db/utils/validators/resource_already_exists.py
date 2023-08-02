from typing import Any
from src.manager__common__db.utils.constants import TKwargs


class ObjectAlreadyExists(Exception):
    def __init__(self, message: str, *args: Any, **kwargs: TKwargs):
        super().__init__(*args, **kwargs)  # type: ignore
        self.message = message
