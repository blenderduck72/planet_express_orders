class InvalidSchemaException(Exception):
    """
    Raised when an invalid Pydantic BaseModel Schema is passed into
    one of the http_decorators
    """
