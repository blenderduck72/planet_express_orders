from src.dynamodb.ModelFactory import CustomerFactory
from src.models.customer import Customer


class TestCustomerFactory:
    def test_customer_factory_gets_customer_by_key(
        self,
        persisted_customer_ddb_dict: dict,
    ) -> None:
        item: dict = CustomerFactory.get_item_by_key(
            {
                "pk": persisted_customer_ddb_dict["pk"],
                "sk": persisted_customer_ddb_dict["sk"],
            }
        )

        assert item
        assert isinstance(item, dict)
        assert item == persisted_customer_ddb_dict

    def test_customer_factory_gets_customer_model_by_key(
        self,
        persisted_customer_ddb_dict: dict,
        customer_data_dict: dict,
    ) -> None:
        customer: Customer = CustomerFactory.get_item_by_key(
            {
                "pk": persisted_customer_ddb_dict["pk"],
                "sk": persisted_customer_ddb_dict["sk"],
            },
            Customer,
        )

        assert customer
        assert isinstance(customer, Customer)
        assert customer == Customer(**customer_data_dict)

    def test_customer_factory_saves_item_from_model(
        self,
        customer_ddb_dict: dict,
        customer_data_dict: dict,
    ):
        customer: Customer = Customer(**customer_data_dict)
        CustomerFactory.save_item_from_model(customer)
        item: dict = CustomerFactory.get_item_by_key(
            CustomerFactory.get_model_key(customer),
        )

        assert item == customer_ddb_dict

    def test_customer_factory_saves_item_from_dict(
        self, customer_data_dict: dict, customer_ddb_dict: dict
    ):
        CustomerFactory.save_item_from_dict(customer_data_dict)

        customer: Customer = Customer(**customer_data_dict)
        item: dict = CustomerFactory.get_item_by_key(
            CustomerFactory.get_model_key(customer),
        )

        assert item == customer_ddb_dict

    def test_customer_factory_updates_items(self, persisted_customer_ddb_dict: dict):
        pass
