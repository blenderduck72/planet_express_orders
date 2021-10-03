from src.models.order import DynamoOrder, Order


class TestDynamoOrder:
    def test_dynamo_order(
        self,
        order_data_dict: dict,
    ) -> None:
        dynamo_order: DynamoOrder = DynamoOrder(**order_data_dict)

        assert dynamo_order
        assert isinstance(dynamo_order, DynamoOrder)
        assert dynamo_order.id
        assert dynamo_order.status == order_data_dict["status"]
        assert (
            dynamo_order.datetime_created.strftime("%Y-%m-%dT%H:%M:%SZ")
            == order_data_dict["datetime_created"]
        )
        assert (
            dynamo_order.delivery_address.dict() == order_data_dict["delivery_address"]
        )


class TestOrder:
    def test_order(
        self,
        order_data_dict: dict,
    ) -> None:
        order: Order = Order(**order_data_dict)
        assert order
        assert isinstance(order, Order)
        assert order
