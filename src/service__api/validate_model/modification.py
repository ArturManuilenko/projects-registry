from pydantic import BaseModel


class ApiProjectModification(BaseModel):
    """Pydantic model"""
    name: str
