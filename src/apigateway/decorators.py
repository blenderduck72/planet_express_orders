from functools import wraps
from typing import Callable

import simplejson as json

from pydantic import BaseModel, ValidationError
from src.apigateway.responses import HttpResponse
from src.apigateway.exceptions import InvalidSchemaException


def http_post_request(schema: BaseModel) -> HttpResponse:
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            event: dict = (
                f_args[0] if not f_kwargs.get("event") else f_kwargs.get("event")
            )

            try:
                raw_data: str = event.get("body")
                data: dict = json.loads(raw_data)
                model: BaseModel = schema(**data)

                return func(model.dict())

            except ValidationError as e:
                return HttpResponse(status_code=422, body=json.dumps(e.errors()))

        return wrapper

    return decorator
