class RemoveLineItemException(Exception):
    """
    Raised when a LineItem cannot be removed from an Order
    """


class CreateCustomerException(Exception):
    """
    Raised when a customer cannot be created
    """


class DuplicateCustomerKeyException(Exception):
    """
    Raised when customer has a duplicate key error
    """


class CustomerLookupException(Exception):
    """
    Raised when a queried customer is not found
    """
