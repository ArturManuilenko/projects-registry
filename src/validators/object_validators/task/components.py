from typing import Optional


def has_components(components: Optional[str]) -> bool:
    if components:
        return True
    raise ValueError('task has not components in Jira')
