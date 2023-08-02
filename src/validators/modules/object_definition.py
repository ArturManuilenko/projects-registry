from importlib import import_module
from typing import NamedTuple, Generic, Type, TypeVar

T = TypeVar('T')


class ObjectDefinition(NamedTuple, Generic[T]):
    module: str
    object_name: str

    def import_object(self) -> Type[T]:
        module_object = import_module(self.module)
        object = getattr(module_object, self.object_name)
        return object
