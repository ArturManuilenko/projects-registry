import enum
from typing import Any, Dict, List


def get_enum_fields(enum: enum.EnumMeta) -> List[Dict[str, Any]]:
    result = []
    for key, _ in enum.__members__.items():
        result.append({'value': getattr(enum, key).value, 'name': key})
    return result
