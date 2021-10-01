import boto3
from boto3.dynamodb.table import TableResource
from ksuid import ksuid

from src.constants import TABLE_NAME
from src.dynamodb.ModelFactory import OrderFactory
from src.models.order import DynamoOrder, OrderStatus
from src.services.exceptions import ServiceCreateItemException


def create_order(
    new_order_data: dict,
) -> DynamoOrder:
    id: ksuid = ksuid()
    new_order_data["id"] = str(id)
    new_order_data["datetime_created"] = id.getDatetime().strftime("%Y-%m-%dT%H:%M:%SZ")

    order_factory: OrderFactory = OrderFactory(new_order_data)

    client = boto3.resource("dynamodb")
    table: TableResource = client.Table(TABLE_NAME)
    try:
        table.put_item(
            Item=order_factory.item,
            ConditionExpression="attribute_not_exists(#pk) and #current_state IN (:#new)",
            ExpressionAttributeNames={
                "#pk": "pk",
                "#new": OrderStatus.NEW,
            },
        )
    except client.meta.client.execptions.ConditionalCheckFailedException as e:
        pass

    return order_factory.model


def get_order():
    pass


def get_orders():
    pass


def update_order():
    pass


def cancel_order():
    pass
