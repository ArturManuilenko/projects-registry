from typing import Any, Union
from uuid import UUID

from werkzeug.routing import BaseConverter, ValidationError


class UUID4Converter(BaseConverter):
    """
    UUID4 converter for the routing system.
    """
    def __init__(self, map: Any) -> None:
        super(UUID4Converter, self).__init__(map)

    def to_python(self, value: Any) -> Union[UUID, None]:
        try:
            return UUID(hex=value, version=4)
        except ValueError:
            raise ValidationError()

    def to_url(self, value: Any) -> str:
        return str(value)
