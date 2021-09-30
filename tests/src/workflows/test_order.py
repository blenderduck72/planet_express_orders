from copy import deepcopy

from src.dynamodb.helpers import get_item
from src.workflows.order import create_order
from src.models.order import DynamoOrder
from src.dynamodb.ModelFactory import OrderFactory


class TestCreateOrder:
    def test_create_order(
        self,
        order_data_dict: dict,
    ):
        new_order_data: dict = deepcopy(order_data_dict)
        new_order_data.pop("id")
        new_order_data.pop("datetime_created")

        dynamo_order: DynamoOrder = create_order(new_order_data)

        assert dynamo_order
        assert isinstance(dynamo_order, DynamoOrder)
        fetched_order: dict = get_item(OrderFactory.get_models_key(dynamo_order))
        assert fetched_order
