from functools import wraps
from typing import Callable

import simplejson as json
from pydantic import BaseModel, ValidationError

from src.apigateway.responses import HttpResponse
from src.apigateway.exceptions import UnkownGetItemMethod
from src.services.base_service import BaseService
from src.models.base_model import DynamoItem


def http_post_request(schema: BaseModel) -> HttpResponse:
    """
    Accepts a Pydantic BaseModel to form from post request data.

        Parameters:
            schema (str): The Pydantic model used for schema validation.

        Returns:
            HttpResponse (HttpResponse): Response of 201 or 422.
    """

    def decorator(func: Callable):
        """
        Decorator accepts a Callable function.

            Parameters:
                func (Callable): The function the decorator is wrapped on.

            Returns:
                HttpResponse (HttpResponse): Response of 201 or 422.
        """

        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            """
            Decorator wrapper accepts wrapped functions args, and kwargs.

                Returns:
                    HttpResponse (HttpResponse): Response of 201 or 422.
            """
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
    model: DynamoItem = DynamoItem,
    get_item_method: str = "get_item_by_key",
) -> HttpResponse:
    """
    Queries DynamoDB to locate an item from path values and return an
    instaniated Pydantic mode of the item.

        Parameters:
            enitity_service (BaseService): The service used to retrieve the DynamoDB item.
            pk_path_parameter (str): The path parameter that contains the the value of the _PK_FIELD
            sk_path_parameter (str): The path parameter that contains the the value of the _SK_FIELD
            model (DynamoItem): The type of Pydantic model to return
            get_item_method (str): The method on the entity_service to retrieve the DynamoDB item.

        Returns:
            HttpResponse (HttpResponse): Response of 201 or 422.
    """

    def decorator(func: Callable):
        """
        Decorator wrapper accepts wrapped functions args, and kwargs.

            Returns:
                HttpResponse (HttpResponse): Response of 201 or 422.
        """

        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            """
            Decorator accepts a Callable function.

                Parameters:
                    func (Callable): The function the decorator is wrapped on.

                Returns:
                    HttpResponse (HttpResponse): Response of 201 or 422.
            """
            event: dict = (
                f_args[0] if not f_kwargs.get("event") else f_kwargs.get("event")
            )
            pk_value: str = event["pathParameters"].get(pk_path_parameter)
            sk_value: str = (
                event["pathParameters"].get(sk_path_parameter)
                if sk_path_parameter
                else None
            )

            key: dict = model.calculate_key(pk_value, sk_value)
            service: BaseService = entity_service()

            method: Callable = getattr(service, get_item_method, None)
            if not method and not callable(method):
                raise UnkownGetItemMethod(
                    f"Unable to locate {get_item_method} on {entity_service.__name__}"
                )

            return func(method(key, model))

        return wrapper

    return decorator
