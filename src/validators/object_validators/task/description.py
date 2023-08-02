from typing import Optional


def has_description(description: Optional[str]) -> bool:
    if description:
        return True
    raise ValueError('task has not description in Jira')
