from datetime import datetime

import boto3

from src.constants import TABLE_NAME
from src.models.customer import Customer
from src.dynamodb.ModelFactory import CustomerFactory
from src.workflows.workflow_exceptions import CreateWorkflowException


def create_customer(
    new_customer_data: dict,
) -> Customer:
    """
    Accepts a new Customer payload and creates a new
    customer if the username is not already in use
    """
    new_customer_data["date_created"] = datetime.now().date().isoformat()

    customer_factory: CustomerFactory = CustomerFactory(new_customer_data)

    client = boto3.resource("dynamodb")
    table = client.Table(TABLE_NAME)

    try:
        table.put_item(
            Item=customer_factory.item,
            ConditionExpression="attribute_not_exists(#username)",
            ExpressionAttributeNames={
                "#username": "username",
            },
        )

    except client.meta.client.exceptions.ConditionalCheckFailedException as e:
        raise CreateWorkflowException("Account already exists")

    return customer_factory.model
