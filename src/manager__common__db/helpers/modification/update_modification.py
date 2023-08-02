from uuid import UUID
from sqlalchemy import and_
from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.manager__common__db.models.modification import Modification


def update_modification(
    name: str,
    project_id: UUID,
    organization_id: UUID,
    modification_id: UUID,
    user_modified_id: UUID
) -> Modification:
    modification_obj = Modification.query.with_deleted().filter(
        and_(
            Modification.organization_id == organization_id,
            Modification.project_id == project_id,
            Modification.id == modification_id
        )
    ).first()

    enshure_db_object_exists(Modification, modification_obj)

    modification_obj.name = name
    modification_obj.mark_as_modified(user_modified_id)
    return modification_obj
