class InvalidSchemaException(Exception):
    """
    Raised when an invalid Pydantic BaseModel Schema is passed into
    one of the http_decorators
    """


class UnkownGetItemMethod:
    """
    Raised when the get_item_method on a parameter is not available in the service.
    """
