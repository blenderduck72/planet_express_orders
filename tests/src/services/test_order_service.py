from copy import deepcopy
from typing import List

from boto3.dynamodb.conditions import Key
import pytest
from pytest import FixtureRequest


from src.dynamodb.helpers import get_item, query_by_key_condition_expression
from src.models.order import DynamoOrder, Order, OrderStatus
from src.dynamodb.ModelFactory import OrderFactory
from src.services.order_service import OrderService
from src.services.exceptions import ServiceCreateItemException


class TestOrderService:
    def test_create_order(
        self,
        order_data_dict: dict,
    ) -> None:
        new_order_data: dict = deepcopy(order_data_dict)
        new_order_data.pop("id")
        new_order_data.pop("datetime_created")
        new_order_data["status"] = OrderStatus.NEW
        client: OrderService = OrderService()

        dynamo_order: DynamoOrder = client.create_order(new_order_data)

        assert dynamo_order
        assert isinstance(dynamo_order, DynamoOrder)
        fetched_order: dict = get_item(OrderFactory.get_models_key(dynamo_order))
        assert fetched_order

    def test_order_adds_line_item_and_increments_item_count(
        self,
        persisted_order_ddb_dict: dict,
        line_item_ddb_dict: dict,
        line_item_data_dict: dict,
    ) -> None:
        order_service: OrderService = OrderService()
        order_service.add_line_item_to_order(
            order_key={
                "pk": persisted_order_ddb_dict["pk"],
                "sk": persisted_order_ddb_dict["sk"],
            },
            new_line_item_data=line_item_data_dict,
        )
        persisted_order_ddb_dict["item_count"] += 1
        items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key("pk").eq(persisted_order_ddb_dict["pk"])
        )

        assert items
        assert line_item_ddb_dict in items
        assert persisted_order_ddb_dict in items

    def test_order_gets_domain_model_by_id(
        self,
        persisted_order_ddb_dict: dict,
        persisted_line_item_ddb_dict: dict,
    ) -> None:
        client: OrderService = OrderService()
        order: Order = client.get_domain_order_by_id(persisted_order_ddb_dict["id"])

        assert isinstance(order, Order)

    @pytest.mark.parametrize(
        "expected_type, expected_result, deserialize",
        [
            (dict, "order_ddb_dict", False),
            (DynamoOrder, "persisted_dynamo_order", True),
        ],
    )
    def test_get_order_by_id(
        self,
        request: FixtureRequest,
        persisted_order_ddb_dict: dict,
        expected_type: dict or DynamoOrder,
        expected_result: str,
        deserialize: bool,
        persisted_dynamo_order: DynamoOrder,
    ):
        expected_value = request.getfixturevalue(expected_result)
        client: OrderService = OrderService()
        response = client.get_order_item_by_id(
            persisted_order_ddb_dict["id"],
            deserialize,
        )

        assert isinstance(expected_value, expected_type)
        assert response == expected_value
