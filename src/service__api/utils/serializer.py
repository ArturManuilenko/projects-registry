from uuid import UUID
from base64 import b64encode
from enum import Enum
from datetime import datetime
from flask_sqlalchemy import BaseQuery
from typing import Dict, Any, Union
from json import JSONEncoder
from flask_sqlalchemy import DefaultMeta
from sqlalchemy.orm import Query
from db_utils.modules.db import db


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj: object) -> Union[str, Dict[str, Any]]:
        if isinstance(obj, db.Model):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                val = obj.__getattribute__(field)
                # is this field method defination, or an SQLalchemy object
                if not hasattr(val, "__call__") and not isinstance(val, BaseQuery):  # noqa: B004
                    if isinstance(val, datetime):
                        val = str(val.isoformat())
                    if isinstance(val, UUID):
                        val = str(val)
                    if isinstance(val, bytes):
                        val = b64encode(val).decode()
                    fields[field] = val
            return fields
        if isinstance(obj, datetime):
            return str(obj.isoformat())
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Enum):
            return str(obj.value)
        if isinstance(obj, Query) or isinstance(obj, DefaultMeta):
            return None
        return super().default(obj)
