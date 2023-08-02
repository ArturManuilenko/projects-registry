from typing import Optional


def has_assignee(user_assignee_id: Optional[str]) -> bool:
    if user_assignee_id:
        return True
    raise ValueError('story task has not selected assignee')
