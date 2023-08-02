from typing import Optional


def has_subtasks(subtasks: Optional[str]) -> bool:
    if subtasks:
        return True
    raise ValueError('task has not subtasks in Jira')
