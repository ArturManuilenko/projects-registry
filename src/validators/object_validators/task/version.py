from typing import Optional


def has_version(version: Optional[str]) -> bool:
    if version:
        return True
    raise ValueError('task has not version in Jira')
