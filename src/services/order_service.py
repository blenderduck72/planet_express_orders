from decimal import Decimal
from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from ksuid import ksuid

from src.constants import TABLE_NAME
from src.dynamodb.ModelFactory import OrderFactory, LineItemFactory
from src.dynamodb.helpers import get_item, put_item, query_by_key_condition_expression
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
        order_factory: OrderFactory = OrderFactory(new_order_data)
        put_item(order_factory.item)

        return order_factory.model

    def update_order(self) -> dict:
        pass

    def get_order_item_by_id(
        self,
        id,
        deserialize=True,
    ) -> dict or DynamoOrder or None:
        pk: str = f"{OrderFactory.PK_ENTITY}#{id}"
        return self.get_order_item_by_key(
            key={"pk": pk, "sk": pk},
            deserialize=deserialize,
        )

    def get_order_item_by_key(
        self, key: dict, deserialize=True
    ) -> dict or DynamoOrder or None:
        item: dict = get_item(key)
        if not deserialize or not item:
            return item

        return OrderFactory(item).model

    def get_domain_order_by_id(
        self,
        id: str,
        deserialize=True,
    ) -> List[dict] or Order:
        items: List[dict] = query_by_key_condition_expression(
            Key("pk").eq(f"{OrderFactory.PK_ENTITY}#{id}")
        )

        if not deserialize:
            return items

        order_dict: dict = {}
        line_items: List[dict] = []

        for item in items:
            if item["entity"] == OrderFactory.PK_ENTITY:
                order_dict = item

            if item["entity"] == LineItemFactory.SK_ENTITY:
                line_items.append(item)

        order_dict["line_items"] = line_items
        return OrderFactory.get_domain_model(order_dict)

    def add_line_item_to_order(
        self,
        order_key: dict,
        new_line_item_data: dict,
    ):
        table = boto3.resource("dynamodb").Table(TABLE_NAME)
        response: dict = table.update_item(
            Key=order_key,
            UpdateExpression="SET #item_count = #item_count + :incr",
            ExpressionAttributeNames={"#item_count": "item_count"},
            ExpressionAttributeValues={":incr": 1},
            ReturnValues="UPDATED_NEW",
        )
        item_count: Decimal = response["Attributes"]["item_count"]
        new_line_item_data["id"] = str(item_count).zfill(2)
        new_line_item_data["order_id"] = order_key["pk"].replace(
            f"{OrderFactory.PK_ENTITY}#", ""
        )
        line_item_factory: LineItemFactory = LineItemFactory(new_line_item_data)
        table.put_item(Item=line_item_factory.item)

    def remove_line_from_order(self):
        pass
