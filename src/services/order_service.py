from typing import List

import boto3
from ksuid import ksuid

from src.constants import TABLE_NAME
from src.dynamodb.ModelFactory import OrderFactory
from src.dynamodb.helpers import put_item
from src.models.order import DynamoOrder, Order, OrderStatus


class OrderService:
    def create_order(
        self,
        new_order_data: dict,
    ) -> DynamoOrder:
        """
        Accpets a new Order payload and creates a new
        Order if the payloads
        """
        id: ksuid = ksuid()
        new_order_data["id"] = str(id)
        new_order_data["datetime_created"] = id.getDatetime().strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        new_order_data["status"] = OrderStatus.NEW
        client = boto3.resource("dynamodb")
        table = client.Table(TABLE_NAME)
        order_factory: OrderFactory = OrderFactory(new_order_data)
        put_item(order_factory.item)

        return order_factory.model

    def update_order(self) -> dict:
        pass

    def get_order_item_by_id(self) -> dict:
        pass

    def get_order_item_by_pk(self) -> dict:
        pass

    def get_domain_order(self) -> List[Order]:
        pass

    def add_line_item_to_order(
        self,
        order_key: dict,
        new_line_item_data: dict,
    ):
        client = boto3.resource("dynamodb").Table(TABLE_NAME)
        client.meta.client.transact_write_items(
            TransactItems=[
                {
                    "Update": {
                        "TableName": TABLE_NAME,
                        "Key": order_key,
                        "UpdateExpression": "SET #item_count = #item_count + :inc",
                        "ExpressionAttributeNames": {"#item_count": "item_count"},
                        "ExpressionAttributeValues": {":inc": 1},
                    },
                }
            ],
        )
