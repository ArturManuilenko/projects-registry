# mypy: ignore-errors
from functools import wraps
from typing import Callable, Any, NamedTuple, Iterable, Dict, List, Tuple

from cached_property import cached_property
from flask import json, request, jsonify
from flask_pydantic.converters import convert_query_params
from flask_pydantic.core import validate_many_models
from flask_pydantic.exceptions import ManyModelValidationError, JsonBodyParsingError
from flask_sqlalchemy import Pagination
from pydantic import ValidationError, BaseModel, parse_obj_as

from src.conf.api_resource import MAX_LIMIT
from src.manager__common__db.utils.response import TJsonResponse
from src.manager__common__db.utils.constants import TKwargs
from src.manager__common__db.utils.validators.resource_error_handler import (
    resource_error_handler_list,
    resource_error_handler_obj
)
from src.manager__common__db.utils.validators.validate_error import ValidateError


class ApiResourcePagination(NamedTuple):
    page: int
    limit: int
    offset: int
    per_page: int

    def mk_sqlalchemy_pagination(self, items: Iterable[Any], total: int, query: Any = None) -> Pagination:
        return Pagination(
            total=total,
            query=query,
            per_page=self.per_page,
            page=self.page,
            items=items,
        )


class ApiResourceSortBy(NamedTuple):
    params: List[Tuple[str, str]]


class ApiResourceFilterBy(NamedTuple):
    params: List[Dict[str, Any]]


class ApiResource:
    def __init__(self, max_limit: int, default_limit: int) -> None:
        self._max_limit = max_limit
        self._default_limit = default_limit

    @cached_property
    def sort_by(self) -> ApiResourceSortBy:
        _sort_args = request.args.get('sort', None)
        _sort_by = []
        if _sort_args:
            _sort_args = _sort_args.split(' ')
            for _sort_arg in _sort_args:
                if _sort_arg:
                    if _sort_arg.startswith("+"):
                        _sort_by.append(("+", _sort_arg[1:]))
                    elif _sort_arg.startswith("-"):
                        _sort_by.append(("-", _sort_arg[1:]))
                    else:
                        _sort_by.append(("+", _sort_arg))
        return ApiResourceSortBy(params=_sort_by)

    @cached_property
    def filter_by(self) -> ApiResourceSortBy:
        _filter_args = request.args.get('filter', None)
        _filter_by = json.loads(_filter_args) if _filter_args else []
        return ApiResourceFilterBy(params=_filter_by)

    @cached_property
    def pagination(self) -> ApiResourcePagination:
        try:
            _limit = request.args.get('limit', None)
            _offset = request.args.get('offset', None)
            _page = request.args.get('page', None)

            page_was_set = _page is not None
            offset_limit_was_set = (_offset is not None) or (_limit is not None)

            wrong_params_of_pagination = page_was_set and offset_limit_was_set

            offset = int(_offset or '0')
            limit = int(_limit or str(self._default_limit))
            page = int(_page or '1')

        except Exception:
            raise ValidateError('invalid pagination parameters. \'limit/offset\' or \'page\' must be int')

        if wrong_params_of_pagination:
            raise ValidateError('invalid pagination parameters. use or \'limit/offset\' or \'page\' params')

        if offset < 0:
            raise ValidateError('invalid offset')

        if page < 1:
            raise ValidateError('invalid page')

        if limit > self._max_limit:
            raise ValidateError(f'invalid limit. should be less than maximum {self._max_limit}')

        if limit <= 0:
            raise ValidateError('invalid limit. should be grate than 0')

        if page_was_set:
            offset = limit * (page - 1)
        else:
            page = int(offset / limit) + 1

        return ApiResourcePagination(
            limit=limit,
            offset=offset,
            page=page,
            per_page=limit,
        )


def _append_errors(errors: List[Dict[str, str]], err: List[Dict[str, str]], kind: str) -> None:
    for e in err:
        errors.append({
            "error_type": kind,
            "error_message": e['msg'],
            "error_location": e["loc"],
            "error_kind": e["type"]
        })


def _validate_query(errors: List[Dict[str, str]], err_kind: str, func: Callable, kwargs: Dict[str, Any]) -> None:
    query_model = func.__annotations__.get("query", None)
    if query_model:
        try:
            kwargs["query"] = query_model(**convert_query_params(request.args, query_model))
        except ValidationError as ve:
            _append_errors(errors, ve.errors(), err_kind)


def _validate_body_many(errors: List[Dict[str, str]], err_kind: str, func: Callable, kwargs: Dict[str, Any]) -> List[BaseModel]:
    body_model = func.__annotations__.get("body")
    if body_model:
        body_params = request.get_json()
        try:
            kwargs['body'] = validate_many_models(body_model, body_params)
        except ManyModelValidationError as e:
            _append_errors(errors, e.errors(), err_kind)
    return []


def _validate_body(errors: List[Dict[str, str]], err_kind: str, func: Callable, kwargs: Dict[str, Any]):
    body_model = func.__annotations__.get("body")
    if body_model:
        if request.form:
            body_params = dict(request.form)
        elif request.get_data().decode('utf-8'):
            body_params = request.get_data().decode('utf-8')
            body_params = json.loads(body_params)
        else:
            body_params = {}
        if "__root__" in body_model.__fields__:
            try:
                kwargs['body'] = body_model(__root__=body_params).__root__
            except ValidationError as ve:
                _append_errors(errors, ve.errors(), err_kind)
        else:
            try:
                kwargs['body'] = body_model(**body_params)
            except TypeError:
                raise JsonBodyParsingError()
            except ValidationError as ve:
                _append_errors(errors, ve.errors(), err_kind)


def _validate_path_params(errors: List[Dict[str, str]], err_kind: str, func: Callable, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    validated = {}
    loc_err = []
    for name, type_ in func.__annotations__.items():
        if name in {"api_resource", "query", "body", "return"}:
            continue
        try:
            value = parse_obj_as(type_, kwargs.get(name))
            validated[name] = value
        except ValidationError as e:
            err = e.errors()[0]
            err["loc"] = [name]
            loc_err.append(err)
    _append_errors(errors, loc_err, err_kind)
    kwargs = {**kwargs, **validated}
    return kwargs


def validated_api_resource_obj(
    max_limit: int = MAX_LIMIT,
    default_limit: int = MAX_LIMIT,
    body_many: bool = False,
) -> Callable[[Callable], Callable[[ApiResource], Any]]:
    def decorate(func: Callable) -> Callable:
        @wraps(func)
        @resource_error_handler_obj
        def wrapper(**kwargs):
            err = []
            kwargs = _validate_path_params(err, "path-params-validation-error", func, kwargs)
            _validate_query(err, "query-validation-error", func, kwargs)
            if body_many:
                _validate_body_many(err, "body-validation-error", func, kwargs)
            else:
                _validate_body(err, "body-validation-error", func, kwargs)

            if len(err) > 0:
                return jsonify({
                    "ok": False,
                    "payload": None,
                    "errors": err
                }), 400

            api_resource = ApiResource(max_limit=max_limit, default_limit=default_limit)
            return func(api_resource, **kwargs)

        return wrapper

    return decorate


def validated_api_resource_list(
    max_limit: int = MAX_LIMIT,
    default_limit: int = MAX_LIMIT,
    body_many: bool = True
) -> Callable[[Callable], Callable[[ApiResource], Any]]:
    def decorate(func: Callable) -> Callable:
        @wraps(func)
        @resource_error_handler_list
        def wrapper(**kwargs):
            err = []
            kwargs = _validate_path_params(err, "path-params-validation-error", func, kwargs)
            _validate_query(err, "query-validation-error", func, kwargs)
            if body_many:
                _validate_body_many(err, "body-validation-error", func, kwargs)
            else:
                _validate_body(err, "body-validation-error", func, kwargs)

            if len(err) > 0:
                return jsonify({
                    "ok": False,
                    "payload": None,
                    "errors": err
                }), 400

            api_resource = ApiResource(max_limit=max_limit, default_limit=default_limit)
            return func(api_resource, **kwargs)

        return wrapper

    return decorate


def api_resource_list(
    max_limit: int = MAX_LIMIT,
    default_limit: int = MAX_LIMIT
) -> Callable[[Callable[..., Any]], Callable[[ApiResource], Any]]:
    def api_resource_list_wrap(fn: Callable[..., Any]) -> Callable[[ApiResource], Any]:
        @wraps(fn)
        @resource_error_handler_list
        def wrapper(*args: Any, **kwargs: TKwargs) -> TJsonResponse:
            api_resource = ApiResource(max_limit=max_limit, default_limit=default_limit)
            return fn(api_resource, *args, **kwargs)

        return wrapper

    return api_resource_list_wrap


def api_resource_obj(
    max_limit: int = MAX_LIMIT,
    default_limit: int = MAX_LIMIT
) -> Callable[[Callable], Callable[[ApiResource], Any]]:
    def api_resource_obj_wrap(fn: Callable) -> Callable[[ApiResource], Any]:
        @wraps(fn)
        @resource_error_handler_obj
        def wrapper(*args: Any, **kwargs: TKwargs) -> TJsonResponse:
            api_resource = ApiResource(max_limit=max_limit, default_limit=default_limit)
            return fn(api_resource, *args, **kwargs)

        return wrapper

    return api_resource_obj_wrap
