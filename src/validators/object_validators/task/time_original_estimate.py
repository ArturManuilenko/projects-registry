from typing import Optional


def has_time_original_estimate(time_original_estimate: Optional[str]) -> bool:
    if time_original_estimate:
        return True
    raise ValueError('task has not time original estimate in Jira')
