from copy import deepcopy

import pytest

from src.dynamodb.helpers import get_item
from src.models.order import DynamoOrder, OrderStatus
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

    def test_order_adds_line_item(
        self,
        persisted_order_ddb_dict: dict,
    ) -> None:
        order_service: OrderService = OrderService()
        order_service.add_line_item_to_order(
            order_key={
                "pk": persisted_order_ddb_dict["pk"],
                "sk": persisted_order_ddb_dict["sk"],
            },
            new_line_item_data=None,
        )
