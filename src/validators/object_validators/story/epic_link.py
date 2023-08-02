from typing import Optional


def has_epic(epic_link: Optional[str]) -> bool:
    if epic_link:
        return True
    raise ValueError('story task has not selected assignee')
