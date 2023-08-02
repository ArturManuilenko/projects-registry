from enum import Enum


class StatusProject(Enum):
    active = "ACTIVE"
    pending = "PENDING"
    stopped = "STOPPED"
    completed = "COMPLETED"
    archived = "ARCHIVED"
