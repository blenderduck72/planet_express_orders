from typing import List

import simplejson as json

from src.apigateway.decorators import (
    http_get_pk_sk_from_path_request,
    http_post_request,
)
from src.apigateway.responses import HttpResponse
from src.models import (
    Customer,
    DynamoAddress,
    DynamoOrder,
    Order,
    OrderStatus,
)
from src.schemas.address import NewAddressSchema
from src.schemas.customer import NewCustomerSchema
from src.schemas.line_item import NewLineItemSchema
from src.schemas.order import NewOrderSchema
from src.services.customer_service import CustomerService
from src.services.exceptions import CreateCustomerException, CustomerLookupException
from src.services.order_service import OrderService


@http_post_request(schema=NewCustomerSchema)
def http_create_customer(
    new_customer_data: dict,
) -> HttpResponse:
    """
    Accepts a Dictionary formatted in the NewCustomerSchema.

        Parameters:
            new_customer_data (dict): Dictionary dump of NewCustomerSchema Pydantic Model.

        Returns:
            HttpResponse (HttpResponse): Response of 201 for newly created customer.

    """
    customer_client: CustomerService = CustomerService()
    try:
        customer: Customer = customer_client.create_customer(new_customer_data)
    except CreateCustomerException:
        return HttpResponse(
            status_code=422,
            body={
                "message": "Unable to create customer.",
            },
        )

    return HttpResponse(
        status_code=201,
        body=customer.json(),
    )


@http_post_request(schema=NewAddressSchema)
def http_add_address_to_customer(
    new_address_data: dict,
    username: str,
) -> HttpResponse:
    """
    Accepts a Dictionary formatted in the NewAddressSchema.

        Parameters:
            new_address_data (dict): Dictionary dump of NewAddressSchema Pydantic Model.

        Returns:
            HttpResponse (HttpResponse): Response of 201 for newly created address.

        Raises:
            CustomerLookupException
    """
    try:
        customer_client: CustomerService = CustomerService()
        address: DynamoAddress = customer_client.add_customer_address(
            username=username,
            new_address_data=new_address_data,
        )
    except CustomerLookupException:
        return HttpResponse(status_code=404, body={"message": "Customer not found"})

    return HttpResponse(status_code=201, body=address.json())


@http_post_request(schema=NewOrderSchema)
def http_create_order(
    new_order_data: dict,
) -> HttpResponse:
    """
    Accepts a Dictionary formatted in the NewOrderSchema.

        Parameters:
            new_order_data (dict): Dictionary dump of NewOrderSchema Pydantic Model.

        Returns:
            HttpResponse (HttpResponse): Response of 201 for newly created Order.

        Raises:
            CustomerLookupException
    """
    try:
        customer_client: CustomerService = CustomerService()
        customer_items: List[dict] = customer_client.get_customer_items_by_email(
            new_order_data["customer_email"]
        )
    except CustomerLookupException:
        return HttpResponse(status_code=422, body={"message": "Customer not found."})

    delivery_address: dict = next(
        (
            item
            for item in customer_items
            if item.get("id") == new_order_data["delivery_address_id"]
        ),
        None,
    )

    if not delivery_address:
        return HttpResponse(422, body={"message": "Invalid delivery_address_id"})

    new_order_data["delivery_address"] = delivery_address
    new_order_data["status"] = OrderStatus.NEW

    order_client: OrderService = OrderService()
    order: DynamoOrder = order_client.create_order(new_order_data)

    return HttpResponse(status_code=201, body=order.json())


@http_get_pk_sk_from_path_request(
    entity_service=OrderService,
    pk_path_parameter="order_id",
    get_item_method="get_domain_order_by_key",
    model=DynamoOrder,
)
def http_get_domain_order(
    order: Order,
) -> HttpResponse:
    """
    Accepts a Domain Order Pydantic Model.

        Parameters:
            new_order_data (dict): Dictionary dump of NewOrderSchema Pydantic Model.

        Returns:
            HttpResponse (HttpResponse): Response of 200 for retrieved Order.

    """
    return HttpResponse(
        status_code=200,
        body=order.json(),
    )


@http_post_request(schema=NewLineItemSchema)
def http_add_line_item(
    new_line_item_data: dict,
    order_id: str,
) -> HttpResponse:
    """
    Accepts a Dictionary formatted in the NewLineItemSchema, and related order_id.

        Parameters:
            order-id (str): Id of the order to add a LineItem to.
            new_order_data (dict): Dictionary dump of NewLineItemSchema Pydantic Model.

        Returns:
            HttpResponse (HttpResponse): Response of 201 for newly created LineItem.

        Raises:
            CustomerLookupException
    """
    order_client: OrderService = OrderService()
    new_line_item_data["order_id"] = order_id
    line_item: dict = order_client.add_line_item_to_order(
        order_key=DynamoOrder.calculate_key(order_id),
        new_line_item_data=new_line_item_data,
    )

    return HttpResponse(
        status_code=201,
        body=json.dumps(line_item),
    )
