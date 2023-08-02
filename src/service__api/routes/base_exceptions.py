from typing import Tuple, Any
from flask import Response as FlaskResponse
from src.service__api.main import app
from src.service__api.utils.response import Response


@app.errorhandler(code_or_exception=404)
def not_found_error(error: Any) -> Tuple[FlaskResponse, int]:
    return Response.not_found_error('URL not found!').send()


@app.errorhandler(code_or_exception=405)
def method_not_allowed_error(error: Any) -> Tuple[FlaskResponse, int]:
    return Response.method_error('Method not allowed!').send()


@app.errorhandler(code_or_exception=500)
def server_error(error: Any) -> Tuple[FlaskResponse, int]:
    return Response.maintance_error('Internal server error!').send()


@app.errorhandler(code_or_exception=503)
def service_unavalible(error: Any) -> Tuple[FlaskResponse, int]:
    return Response.maintance_error('Service temporarily unavailable').send()
