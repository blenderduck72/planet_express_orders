from decimal import Decimal
from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from ksuid import ksuid

from src.dynamodb.helpers import get_item, put_item, query_by_key_condition_expression
from src.models import (
    DynamoOrder,
    LineItem,
    Order,
    OrderStatus,
)
from src.models.address import DynamoAddress
from src.services.base_service import BaseService
from src.services.exceptions import RemoveLineItemException


class OrderService(BaseService):
    """
    Represents Order Service.

    ...

    Attributes
    ----------
    FACTORY : OrderFactory
        ItemFactory used by obtain root Model's Key
    TABLE_NAME: str
        DynamoDB Table Name utilized by service.


    Methods
    -------
    get_factory_item_by_key(key: dict) -> ItemFactory
        Retrieves a specific DynamoDB item and returns it
        wrapped in an ItemFactory

    add_line_item_to_order(order_key: dict, new_line_item_data: dict) -> dict
        Adds a LineItem to an Order.

    create_order(new_order_data: dict) -> DynamoOrder
        Creates and returns the DynamoDB representation of an Order.

    get_domain_order_by_id(id: str, deserialize: bool=true) -> List[dict] or Order
        Retrieves the aggregate list of entities that makeup a domain
        Order and return the list or utilize the list to instantiate a
        pydantic Order.

    get_domain_order_by_key(key: dict, deserialize: bool) -> True
        Retrieves the aggregate list of entities that makeup a domain
        Order and return the list or utilize the list to instantiate a
        pydantic Order.

    get_order_key_from_id(id: str) -> dict
        Calculates and returns what should be a LineItem's dynamodb key.

    get_order_item_by_id(id: str, deserialize: bool = True) -> dict or DynamoOrder or None
        Returns an Order from its id as either a dict or instantiated
        DynamoOrder

    get_order_item_by_key(id: str, deserialize: bool = True) -> dict or DynamoOrder or None
        Returns an Order from its DyanmoDb key as either a dict or instantiated
        DynamoOrder

    remove_line_item_from_order(order_id: str, line_item_id: int) -> None
        Deletes an Order's LineItem.

    """

    def add_line_item_to_order(
        self,
        order_key: dict,
        new_line_item_data: dict,
    ) -> dict:
        """
        Adds a LineItem to an Order entity, and imcrements
        an Order's item_count by 1

        Parameters:
            order_key (dict): DyanamoDB key of order {'pk':'value', 'sk':'value'}.
            new_line_item_data: (dict): Dictionary of LineItem data (NewLineItemSchema).

        Returns:
            line_item_dict (dict): A Dictionary that represents the saved LineItem.
        """
        table = boto3.resource("dynamodb").Table(self.TABLE_NAME)

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
            f"{DynamoOrder._PK_ENTITY}#", ""
        )
        line_item: dict = LineItem(**new_line_item_data).item
        table.put_item(Item=line_item)
        return line_item

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
        order: DynamoOrder = DynamoOrder(**new_order_data)
        put_item(order.item, self.TABLE_NAME)

        return order

    def get_domain_order_by_id(
        self,
        id: str,
        deserialize=True,
    ) -> List[dict] or Order:
        items: List[dict] = query_by_key_condition_expression(
            Key("pk").eq(f"{DynamoOrder._PK_ENTITY}#{id}"),
            table_name=self.TABLE_NAME,
        )

        if not items:
            return None

        if not deserialize:
            return items

        order_dict: dict = {}
        line_items: List[dict] = []

        for item in items:
            if item["entity"] == DynamoOrder._PK_ENTITY:
                order_dict = item

            if item["entity"] == LineItem._SK_ENTITY:
                line_items.append(item)

        order_dict["line_items"] = line_items

        return Order(**order_dict)

    def get_domain_order_by_key(
        self,
        key: dict,
        *args,
    ) -> Order:

        return self.get_domain_order_by_id(
            key["pk"].replace(f"{DynamoOrder._PK_ENTITY}#", "")
        )

    @classmethod
    def get_order_key_from_id(
        cls,
        id: str,
    ) -> dict:
        pk_value: str = f"{DynamoOrder._PK_ENTITY}#{id}"
        return {"pk": pk_value, "sk": pk_value}

    def get_order_item_by_id(
        self,
        id,
        deserialize=True,
    ) -> dict or DynamoOrder or None:

        return self.get_order_item_by_key(
            key=DynamoOrder.calculate_key(id),
            deserialize=deserialize,
        )

    def get_order_item_by_key(
        self, key: dict, deserialize=True
    ) -> dict or DynamoOrder or None:
        item: dict = get_item(key, self.TABLE_NAME)
        if not deserialize or not item:
            return item

        return DynamoOrder(**item)

    def remove_line_from_order(
        self,
        order_id: str,
        line_item_id: int,
    ) -> None:
        order_key: dict = self.get_order_key_from_id(order_id)
        line_item_key: dict = LineItem.calculate_key(order_id, line_item_id)

        client = boto3.resource("dynamodb").Table(self.TABLE_NAME)

        try:
            client.meta.client.transact_write_items(
                TransactItems=[
                    {
                        "Update": {
                            "TableName": self.TABLE_NAME,
                            "Key": order_key,
                            "UpdateExpression": "SET #item_count = #item_count - :inc",
                            "ExpressionAttributeNames": {
                                "#item_count": "item_count",
                                "#status": "status",
                            },
                            "ExpressionAttributeValues": {
                                ":inc": 1,
                                ":new": OrderStatus.NEW,
                            },
                            "ConditionExpression": "#status IN (:new)",
                        },
                    },
                    {
                        "Delete": {
                            "TableName": self.TABLE_NAME,
                            "Key": line_item_key,
                            "ConditionExpression": "attribute_exists(sk)",
                        },
                    },
                ],
            )
        except client.meta.client.exceptions.TransactionCanceledException:
            raise RemoveLineItemException("Unable to remove line_item from Order")
