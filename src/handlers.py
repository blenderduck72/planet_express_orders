from typing import List

from src.apigateway.decorators import (
    http_get_pk_sk_from_path_request,
    http_post_request,
)
from src.apigateway.responses import HttpResponse
from src.models import (
    Customer,
    DynamoOrder,
    Order,
    OrderStatus,
)
from src.schemas.order import NewOrderSchema
from src.schemas.customer import NewCustomerSchema
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService
from src.services.exceptions import CreateCustomerException, CustomerLookupException


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


@http_post_request(schema=NewOrderSchema)
def http_create_order(
    new_order_data: dict,
) -> HttpResponse:

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
)
def http_get_domain_order(
    order: Order,
) -> HttpResponse:
    return HttpResponse(
        status_code=200,
        body=order.json(),
    )
