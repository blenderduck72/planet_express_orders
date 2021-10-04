from copy import deepcopy
from typing import List

import pytest
from boto3.dynamodb.conditions import Key

from src.dynamodb.helpers import get_item, query_by_key_condition_expression
from src.dynamodb.ModelFactory import CustomerFactory
from src.models.customer import Customer
from src.services.customer_service import CustomerService
from src.services.exceptions import CreateCustomerException


class TestCustomerService:
    def test_create_customer_succeeds(
        self,
        customer_data_dict: dict,
        customer_ddb_dict: dict,
    ) -> None:
        new_customer_data: dict = deepcopy(customer_data_dict)
        customer_factory: CustomerFactory = CustomerFactory(customer_data_dict)
        new_customer_data.pop("date_created")

        customer_client: CustomerService = CustomerService()
        customer_model: Customer = customer_client.create_customer(customer_data_dict)

        fetched_customer: dict = get_item(customer_factory.key)

        assert fetched_customer
        fetched_customer.pop("date_created")
        customer_ddb_dict.pop("date_created")

        assert fetched_customer == customer_ddb_dict
        assert isinstance(customer_model, Customer)

    def test_create_customer_raises_exception(
        self,
        customer_data_dict: dict,
        persisted_customer_ddb_dict: dict,
    ) -> None:
        new_customer_data: dict = deepcopy(customer_data_dict)
        new_customer_data.pop("date_created")
        customer_client: CustomerService = CustomerService()

        with pytest.raises(CreateCustomerException):
            customer_client.create_customer(new_customer_data)

    def test_add_customer_address(
        self,
        persisted_customer_ddb_dict: dict,
        new_address_data_dict: dict,
    ) -> None:
        customer_client: CustomerService = CustomerService()
        customer_client.add_customer_address(
            persisted_customer_ddb_dict["username"],
            new_address_data_dict,
        )

        customer_items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key("pk").eq(persisted_customer_ddb_dict["pk"])
        )

        assert len(customer_items) == 2


def test_bob():
    some_data: dict = {
        "email": "philipfry@planetexpress.com",
        "first_name": "philip",
        "last_name": "fry",
        "username": "pfry",
        "date_created": "2021-10-04",
    }
    customer_factory = CustomerFactory(some_data)
    import pdb

    pdb.set_trace()
