from typing import NamedTuple, List, Any, Union, Tuple
from flask import jsonify
from flask import Response as FlaskResponse


class ResponseError(NamedTuple):
    error_type: str
    error_message: str

    @staticmethod
    def access_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="access-error", error_message=msg)

    @staticmethod
    def auth_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="auth-error", error_message=msg)

    @staticmethod
    def jwt_auth_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="jwt_auth-error", error_message=msg)

    @staticmethod
    def bad_request_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="bad-request-error", error_message=msg)

    @staticmethod
    def maintance_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="maintance-error", error_message=msg)

    @staticmethod
    def method_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="method-error", error_message=msg)

    @staticmethod
    def missing_data_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="missing-data-error", error_message=msg)

    @staticmethod
    def not_found_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="not-found-error", error_message=msg)

    @staticmethod
    def valid_err(msg: str) -> 'ResponseError':
        return ResponseError(error_type="validation-error", error_message=msg)


class Response(NamedTuple):
    ok: bool = None
    payload: Union[List[Any], Any, None] = None
    errors: List[ResponseError] = []

    def send(self) -> Tuple[FlaskResponse, int]:
        if len(self.errors) > 0:
            if self.errors[0].error_type == 'auth-error':
                return self.format_response(self, 401)
            if self.errors[0].error_type == 'jwt-auth-error':
                return self.format_response(self, 401)
            elif self.errors[0].error_type == 'access-error':
                return self.format_response(self, 403)
            elif self.errors[0].error_type == 'not-found-error':
                return self.format_response(self, 404)
            elif self.errors[0].error_type == 'method-error':
                return self.format_response(self, 405)
            elif self.errors[0].error_type == 'maintance-error':
                return self.format_response(self, 503)
            return self.format_response(self, 400)
        return self.format_response(self, 200)

    @staticmethod
    def access_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.access_err(message)])

    @staticmethod
    def auth_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.auth_err(message)])

    @staticmethod
    def jwt_auth_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.jwt_auth_err(message)])

    @staticmethod
    def bad_request_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.bad_request_err(message)])

    @staticmethod
    def maintance_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.maintance_err(message)])

    @staticmethod
    def method_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.method_err(message)])

    @staticmethod
    def missing_data_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.missing_data_err(message)])

    @staticmethod
    def not_found_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.not_found_err(message)])

    @staticmethod
    def validation_error(message: str) -> 'Response':
        return Response(errors=[ResponseError.valid_err(message)])

    @staticmethod
    def format_response(resp: 'Response', status_code: int) -> Tuple[FlaskResponse, int]:
        # set ok from responce
        # or automatically set ok by status code
        if not resp.ok:
            is_ok = True if 200 <= status_code < 400 else False
        else:
            is_ok = resp.ok

        return (
            jsonify({
                "ok": is_ok,
                "payload": resp.payload,
                "errors": [{"error_type": er.error_type, "error_message": er.error_message} for er in resp.errors]
            }),
            status_code
        )
