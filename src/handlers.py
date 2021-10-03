import json

from src.apigateway.decorators import http_post_request
from src.apigateway.responses import HttpResponse
from src.services.customer_service import CustomerService
from src.services.exceptions import CreateCustomerException
from src.schemas.customer import NewCustomerSchema
from src.models.customer import Customer


def hello(event, context):
    body = {
        "message": "Go Serverless v2.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}


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
