from typing import Tuple

from flask import request

from src.manager__common__db.utils.validators.validate_error import ValidateError


def request_limit_offset(max_limit: int = 1000) -> Tuple[int, int]:
    try:
        limit = int(request.args.get('limit', str(max_limit)))
        offset = int(request.args.get('offset', '0'))
    except Exception:
        raise ValidateError('invalid parameter')

    if offset < 0:
        raise ValidateError('invalid offset')

    if limit > max_limit:
        raise ValidateError(f'invalid limit. should be less than maximum {max_limit}')

    if limit <= 0:
        raise ValidateError('invalid limit. should be grate than 0')

    return limit, offset


def transform_limit_offset_to_page(limit: int, offset: int) -> Tuple[int, int]:
    return int(offset / limit), limit
