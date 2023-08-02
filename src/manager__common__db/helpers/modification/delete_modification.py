from uuid import UUID
from sqlalchemy import and_
from src.manager__common__db.models.modification import Modification


def delete_modification(
    modification_id: UUID,
    organization_id: UUID,
    project_id: UUID,
    user_deleted_id: UUID
) -> None:
    modification_release_obj = Modification.query.filter(
        and_(
            Modification.id == modification_id,
            Modification.project_id == project_id,
            Modification.organization_id == organization_id
        )
    ).first()
    if modification_release_obj is not None:
        modification_release_obj.mark_as_deleted(user_deleted_id)
