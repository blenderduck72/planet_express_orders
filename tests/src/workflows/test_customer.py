from copy import deepcopy

import pytest

from src.dynamodb.ModelFactory import CustomerFactory
from src.models.customer import Customer
from src.workflows.customer import create_customer
from src.workflows.workflow_exceptions import CreateWorkflowException


class TestCreateCustomer:
    def test_create_customer_succeeds(
        self, customer_data_dict: dict, customer_ddb_dict: dict
    ):
        new_customer_data: dict = deepcopy(customer_data_dict)
        new_customer_data.pop("date_created")

        customer: Customer = create_customer(customer_data_dict)
        fetched_customer: dict = CustomerFactory.get_item_dict_by_model(customer)

        assert fetched_customer
        fetched_customer.pop("date_created")
        customer_ddb_dict.pop("date_created")
        assert fetched_customer == customer_ddb_dict

    def test_create_customer_raises_exception(
        self,
        customer_data_dict: dict,
        persisted_customer_ddb_dict: dict,
    ):
        new_customer_data: dict = deepcopy(customer_data_dict)
        new_customer_data.pop("date_created")

        with pytest.raises(CreateWorkflowException):
            create_customer(new_customer_data)
