from typing import Optional


def has_expected_result(expected_result: Optional[str]) -> bool:
    if expected_result:
        return True
    raise ValueError('task has not expected_result in Jira')
