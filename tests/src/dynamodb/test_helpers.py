from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import _Table

from src.constants import TABLE_NAME
from src.dynamodb.helpers import (
    get_item,
    put_item,
    query_by_key_condition_expression,
)


class TestPutItem:
    def test_put_item(
        self,
        order_ddb_dict: dict,
    ) -> None:
        put_item(order_ddb_dict)

        table: _Table = boto3.resource("dynamodb").Table(TABLE_NAME)
        response: dict = table.get_item(
            Key={
                "pk": order_ddb_dict["pk"],
                "sk": order_ddb_dict["sk"],
            }
        ).get("Item")

        assert response
        assert response == order_ddb_dict


class TestGetItem:
    def test_get_item(
        self,
        persisted_order_ddb_dict: dict,
    ) -> None:
        item: dict = get_item(
            {
                "pk": persisted_order_ddb_dict["pk"],
                "sk": persisted_order_ddb_dict["sk"],
            }
        )

        assert item
        assert item == persisted_order_ddb_dict


class TestQueryByKeyConditionExpression:
    def test_query_by_key_condition_expression(
        self,
        persisted_order_ddb_dict: dict,
    ) -> None:
        items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key("pk").eq(persisted_order_ddb_dict["pk"])
            & Key("sk").begins_with("Order#")
        )

        assert items
        assert isinstance(items, list)
        assert persisted_order_ddb_dict in items
