import os
import json
import functools
from typing import Any, Callable, Dict, Tuple
from datetime import datetime
from src.service__api.utils.serializer import CustomJSONEncoder


def cache_result(fn: Callable[..., Any] = None, *, ttl: int = 60) -> Any:  # can return any function result type
    """
    Crutch function for chache result of function
    and get cache from .json file time of ttl
    """
    if fn is None:
        return functools.partial(cache_result, ttl=ttl)

    cache = {}
    cache_path = f'../.tmp/cache/{id(fn)}.json'
    cache_time = datetime.fromordinal(1)

    @functools.wraps(fn)
    def inner(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:  # can return any function result type
        nonlocal cache, cache_time
        now = datetime.now()

        # check cache file exist, if not create them
        if not os.path.exists(cache_path):
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            os.mknod(cache_path)

        # get date_created of cache file
        with open(cache_path, 'r+') as cache_file:
            try:
                cache_from_file = json.load(cache_file)
                cache_time = datetime.fromisoformat(cache_from_file.get('date_created'))
                last_kwargs = cache_from_file.get('kwargs')
            except json.decoder.JSONDecodeError:
                last_kwargs = kwargs
                cache_time = datetime.fromordinal(1)
        if (ttl < (now - cache_time).total_seconds()) or not last_kwargs == kwargs:
            try:
                cache['payload'] = fn(*args, **kwargs)
            except Exception:
                cache['payload'] = None
            with open(cache_path, 'w') as cache_file:
                cache['date_created'] = datetime.now()
                cache['kwargs'] = kwargs
                json.dump(cache, cache_file, cls=CustomJSONEncoder)
        else:
            with open(cache_path, 'r') as cache_file:
                cache['payload'] = json.load(cache_file).get('payload')
        return cache.get("payload")
    return inner
