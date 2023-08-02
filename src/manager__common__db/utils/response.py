from typing import Tuple, Dict, Any, Iterable

from flask import jsonify
from flask import Response

TJsonResponse = Tuple[Response, int]
TJsonObj = Dict[str, Any]


def response_list_ok(list_of_obj: Iterable[Any], total_count: int) -> TJsonResponse:
    objs = list(list_of_obj)
    return jsonify(dict(
        ok=True,
        payload=objs,
        count=len(objs),
        total_count=total_count,
        errors=[],
    )), 200


def response_obj_ok(obj: Any) -> TJsonResponse:
    return jsonify(dict(
        ok=True,
        payload=obj,
        errors=[],
    )), 200


def response_obj_deleted_ok() -> TJsonResponse:
    return jsonify(dict(
        ok=True,
        payload=[],
        errors=[],
    )), 201


def response_obj_created_ok(obj: Any) -> TJsonResponse:
    return jsonify(dict(
        ok=True,
        payload=obj,
        errors=[],
    )), 201


def response_obj_not_found() -> TJsonResponse:
    return jsonify(dict(
        ok=False,
        payload=None,
        errors=['No resource was found that matches the request URI'],
    )), 404


def response_obj_with_such_mac_and_protocol_already_exist() -> TJsonResponse:
    return jsonify(dict(
        ok=False,
        payload=None,
        errors=['Object with such protocol name and mac already exist'],
    )), 404
