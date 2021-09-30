from ksuid import ksuid

from src.constants import TABLE_NAME
from src.dynamodb.helpers import put_item
from src.dynamodb.ModelFactory import OrderFactory
from src.models.order import DynamoOrder
from src.workflows.workflow_exceptions import CreateWorkflowException


def create_order(
    new_order_data: dict,
) -> DynamoOrder:
    id: ksuid = ksuid()
    new_order_data["id"] = str(id)
    new_order_data["datetime_created"] = id.getDatetime().strftime("%Y-%m-%dT%H:%M:%SZ")

    order_factory: OrderFactory = OrderFactory(new_order_data)
    put_item(order_factory.item)

    return order_factory.model


def update_order():
    pass


def cancel_order():
    pass
