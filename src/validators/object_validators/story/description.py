from typing import Any, Optional


def has_description(description: Optional[Any]) -> bool:
    if not description:
        raise ValueError('story task has not description')
    if len(description) < 100:
        raise ValueError('story task description length have less then 100 symbols')
    return True
