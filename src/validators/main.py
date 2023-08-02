import os
from types import FunctionType
import yaml
from typing import Any, List, Optional, Dict

from src.validators.utils.parse_definition import parse_definition
from src.validators.utils.parse_type import parse_type
from src.validators.utils.template import template


class Validator():
    def __init__(self) -> None:
        self.__config_file_path__ = os.path.join(os.path.dirname(__file__), 'structure.yml')
        with open(self.__config_file_path__, 'rt') as f:
            self._config = yaml.safe_load(f)
        self._instances = [instance for instance in parse_definition(self._config['instance'])]

    def _validate_dict_item(self, item: Dict[str, Any], validate_functons: List[Dict[FunctionType, List[str]]]) -> List[Dict[str, str]]:
        errors = []
        if isinstance(item, dict):
            for _validator in validate_functons:
                validate_function, fields = list(_validator.items())[0]
                try:
                    if len(fields) == 1:
                        validate_function(item.get(fields[0], None))
                    elif len(fields) > 1:
                        validate_function(*[item.get(field, None) for field in fields])
                    else:
                        raise TypeError(f'Funtion {validate_function} have invalid fields count in structure.yml')
                except ValueError as validation_error:
                    errors.append({
                        'error_type': validate_function.__name__,
                        'error_message': validation_error.args[0]
                    })
        return errors

    def _validate_object_item(self, item: object, validate_functons: List[Dict[FunctionType, List[str]]]) -> List[Dict[str, str]]:
        errors = []
        if isinstance(item, dict):
            for _validator in validate_functons:
                validate_function, fields = list(_validator.items())[0]
                try:
                    if len(fields) == 1:
                        validate_function(getattr(item, fields[0], None))
                    elif len(fields) > 1:
                        validate_function(*[getattr(item, field, None) for field in fields])
                    else:
                        raise TypeError(f'Funtion {validate_function} have invalid fields count in structure.yml')
                except ValueError as validation_error:
                    errors.append({
                        'error_type': validate_function.__name__,
                        'error_message': validation_error.args[0]
                    })
        return errors

    def _parse_instance_validations(self, instance_name: str) -> Dict[str, Any]:
        try:
            return self._parse_instance(parse_definition(self._config['instance'])[instance_name])
        except KeyError:
            raise ValueError(f'Instance {instance_name} validate funtions described in structure.yml not found')

    def _parse_instance(self, definition: Dict[str, Any]) -> Dict[Any, str]:
        result = dict()
        try:
            result.update({'type': parse_type(template(definition['type'], definition)).import_object()})
        except ModuleNotFoundError:
            pass
        result.update({'name': definition['name']})
        result.update({'validate_fields_methods': []})
        for method, fields in definition['validate_fields_methods'].items():
            if isinstance(fields, list):
                result['validate_fields_methods'].append({parse_type(method).import_object(): [field for field in fields]})
            else:
                result['validate_fields_methods'].append({parse_type(method).import_object(): fields})
        return result

    def validate_project(self, project: Dict[str, Any]) -> List[Optional[Dict[str, str]]]:
        self._project_validators = self._parse_instance_validations('project')['validate_fields_methods']
        return self._validate_dict_item(project, self._project_validators)

    def validate_task(self, task: Dict[str, Any]) -> List[Optional[Dict[str, str]]]:
        taks_validators = self._parse_instance_validations('task')['validate_fields_methods']
        return self._validate_dict_item(task, taks_validators)

    def validate_epic(self, epic: Dict[str, Any]) -> List[Optional[Dict[str, str]]]:
        epic_validators = self._parse_instance_validations('epic')['validate_fields_methods']
        return self._validate_dict_item(epic, epic_validators)

    def validate_bug(self, bug: Dict[str, Any]) -> List[Optional[Dict[str, str]]]:
        bug_validators = self._parse_instance_validations('bug')['validate_fields_methods']
        return self._validate_dict_item(bug, bug_validators)

    def validate_stories(self, stories: Dict[str, Any]) -> List[Optional[Dict[str, str]]]:
        stories_validators = self._parse_instance_validations('story')['validate_fields_methods']
        return self._validate_dict_item(stories, stories_validators)

    def validate_releases(self, release: Dict[str, Any]) -> List[Optional[Dict[str, str]]]:
        release_validators = self._parse_instance_validations('release')['validate_fields_methods']
        return self._validate_dict_item(release, release_validators)
