from typing import Optional


def has_selected_assignee(user_assignee_id: Optional[str]) -> bool:
    if user_assignee_id:
        return True
    raise ValueError('task has not selected assignee in Jira')
