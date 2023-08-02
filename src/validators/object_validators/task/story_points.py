from typing import Optional


def has_story_points(story_points: Optional[str]) -> bool:
    if story_points:
        return True
    raise ValueError('task has not story points in Jira')
