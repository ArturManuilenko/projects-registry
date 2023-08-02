from functools import wraps
from typing import Callable, Any

from flask import jsonify
from pydantic import PydanticValueError

from src.manager__common__db.utils.response import TJsonResponse
from src.manager__common__db.utils.constants import TKwargs
from src.manager__common__db.utils.validators.validate_error import ValidateError
from sqlalchemy.orm.exc import NoResultFound

from src.manager__common__db.utils.validators.resource_already_exists import ObjectAlreadyExists


def resource_error_handler_obj(fn: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: TKwargs) -> TJsonResponse:
        try:
            return fn(*args, **kwargs)
        except ValidateError as e:
            return jsonify({
                "ok": False,
                "payload": None,
                "errors": [
                    {"error_type": "body-validation-error", "error_message": str(e.message)}  # noqa: B306
                ]
            }), 400
        except NoResultFound:
            return jsonify({
                "ok": False,
                "payload": None,
                "errors": [
                    {"error_type": "body-validation-error", "error_message": "Resource isn't exist"}
                ]
            }), 404
        except ObjectAlreadyExists:
            return jsonify({
                "ok": False,
                "payload": None,
                'errors': [
                    {
                        "error_kind": "value_error.alredy_exist",
                        "error_type": "body-validation-error",
                        "error_message": "Object already exist"
                    }
                ]
            }), 400
        except PydanticValueError as e:
            return jsonify({
                "ok": False,
                "payload": None,
                'errors': [
                    {
                        "error_kind": f"value_error.{e.code}",
                        "error_location": [f"{e.location}"],    # type: ignore
                        "error_type": "body-validation-error",
                        "error_message": f"{e.msg_template}"
                    }
                ]
            }), 400

    return wrapper


def resource_error_handler_list(fn: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: TKwargs) -> TJsonResponse:
        try:
            return fn(*args, **kwargs)
        except ValidateError as e:
            return jsonify({
                "ok": False,
                "payload": [],
                "errors": [{"error_type": "validation-error", "error_message": str(e.message)}]  # noqa: B306
            }), 400
        except NoResultFound:
            return jsonify({
                "ok": False,
                "payload": None,
                "errors": [
                    {"error_type": "validation-error", "error_message": "Resource doesn't exist"},
                ]
            }), 404

    return wrapper
