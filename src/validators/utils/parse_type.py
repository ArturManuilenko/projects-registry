from src.validators.modules.object_definition import ObjectDefinition


def parse_type(type_definition: str) -> ObjectDefinition:
    assert isinstance(type_definition, str), f"type_def must be str. {type(type_definition)} given"
    spec = type_definition.split(":")
    assert len(spec) == 2, f'must have 2 segments. {len(spec)} was given from "{type_definition}"'
    return ObjectDefinition(
        module=spec[0],
        object_name=spec[1],
    )
