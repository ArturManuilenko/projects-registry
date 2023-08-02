from uuid import UUID
from db_utils.modules.db import db
from src.manager__common__db.models.modification import Modification


def add_new_modification(
        organization_id: UUID,
        project_id: UUID,
        name: str,
        user_created_id: UUID
) -> Modification:
    new_modification = Modification(
        organization_id=organization_id,
        project_id=project_id,
        name=name
    )
    new_modification.mark_as_created(user_created_id)
    db.session.add(new_modification)
    return new_modification
