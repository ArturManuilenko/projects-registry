from typing import Dict, Any
from jinja2 import Environment, BaseLoader


def template(definition: str, data: Dict[str, Any]) -> str:
    assert isinstance(definition, str), f"definition must be str. {type(definition)} given"

    env = Environment(loader=BaseLoader())
    rtemplate = env.from_string(definition)
    result = rtemplate.render(**data)

    return result
