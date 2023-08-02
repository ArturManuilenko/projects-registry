# -*- coding: utf-8 -*-
"""The root of JIRA package namespace."""
try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("jira").version
except Exception:
    __version__ = "unknown"

from .client import JIRA  # noqa: E402
from .client import Comment  # noqa: E402
from .client import Issue  # noqa: E402
from .client import Priority  # noqa: E402
from .client import Project  # noqa: E402
from .client import Role  # noqa: E402
from .client import User  # noqa: E402
from .client import Watchers  # noqa: E402
from .client import Worklog  # noqa: E402
from .config import get_jira  # noqa: E402
from .exceptions import JIRAError  # noqa: E402

__all__ = (
    "Comment",
    "__version__",
    "Issue",
    "JIRA",
    "JIRAError",
    "Priority",
    "Project",
    "Role",
    "User",
    "Watchers",
    "Worklog",
    "get_jira",
)
