from functools import wraps
from typing import Callable

import simplejson as json
from pydantic import BaseModel, ValidationError

from src.apigateway.responses import HttpResponse
from src.apigateway.exceptions import UnkownGetItemMethod
from src.services.base_service import BaseService


def http_post_request(schema: BaseModel) -> HttpResponse:
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            event: dict = (
                f_args[0] if not f_kwargs.get("event") else f_kwargs.get("event")
            )
            path_parametrs: dict = event.get("pathParameters")

            try:
                raw_data: str = event.get("body")
                data: dict = json.loads(raw_data)
                model: BaseModel = schema(**data)
                if path_parametrs:
                    return func(model.dict(), **path_parametrs)
                return func(model.dict())

            except ValidationError as e:
                return HttpResponse(status_code=422, body=json.dumps(e.errors()))

        return wrapper

    return decorator


def http_get_pk_sk_from_path_request(
    entity_service: BaseService,
    pk_path_parameter: str,
    sk_path_parameter: str or None = None,
    get_item_method: str = "get_factory_item_by_key",
) -> HttpResponse:
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            event: dict = (
                f_args[0] if not f_kwargs.get("event") else f_kwargs.get("event")
            )
            pk_value: str = event["pathParameters"].get(pk_path_parameter)
            sk_value: str = (
                event["pathParameters"].get(sk_path_parameter)
                if sk_path_parameter
                else None
            )

            key: dict = entity_service.FACTORY.calculate_key(pk_value, sk_value)
            service: BaseService = entity_service()

            method: Callable = getattr(service, get_item_method, None)
            if not method and not callable(method):
                raise UnkownGetItemMethod(
                    f"Unable to locate {get_item_method} on {entity_service.__name__}"
                )

            return func(method(key))

        return wrapper

    return decorator
