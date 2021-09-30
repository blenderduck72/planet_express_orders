from src.models.order import Order


class TestOrder:
    def test_order(
        self,
        order_data_dict: dict,
    ):
        order: Order = Order(**order_data_dict)
