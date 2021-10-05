from copy import deepcopy

import pytest
import simplejson as json
from src.dynamodb.ModelFactory import LineItemFactory

from src.dynamodb.helpers import get_item
from src.handlers import (
    http_add_address_to_customer,
    http_add_line_item,
    http_create_customer,
    http_create_order,
    http_get_domain_order,
)
from src.models.order import Order, OrderStatus
from src.services.order_service import OrderService


class TestHttpCreateCustomer:
    @pytest.mark.freeze_time
    def test_http_create_customer_succeeds(
        self,
        customer_data_dict: dict,
        new_customer_data_dict: dict,
    ) -> None:
        response: dict = http_create_customer(
            event={
                "body": json.dumps(new_customer_data_dict),
            },
            context=None,
        )

        assert response["statusCode"] == "201"
        assert json.loads(response["body"]) == customer_data_dict

    def test_http_create_customer_returns_422_with_extra_data(
        self,
        new_customer_data_dict,
    ) -> None:
        new_customer_data_dict["key_that_should_not"] = "be_here"

        response: dict = http_create_customer(
            event={"body": json.dumps(new_customer_data_dict)}, context=None
        )

        assert response["statusCode"] == "422"

    def test_http_create_customer_raises_422_with_bad_data(
        self,
        new_customer_data_dict: dict,
    ) -> None:
        new_customer_data_dict["email"] = "definately not an email"
        response: dict = http_create_customer(
            event={"body": json.dumps(new_customer_data_dict)}, context=None
        )

        assert response["statusCode"] == "422"
        assert (
            response["body"]
            == '[{"loc": ["email"], "msg": "value is not a valid email address", "type": "value_error.email"}]'
        )

    def test_http_create_customer_fails_when_customer_already_exists(
        self,
        new_customer_data_dict: dict,
        persisted_customer_ddb_dict: dict,
    ) -> None:
        response: dict = http_create_customer(
            event={
                "body": json.dumps(new_customer_data_dict),
            },
            context=None,
        )

        assert response["statusCode"] == "422"
        assert json.loads(response["body"]) == {
            "message": "Unable to create customer.",
        }


class TestHttpAddAddressToCustomer:
    def test_add_address_to_customer_succeeds(
        self,
        new_address_data_dict: dict,
        persisted_customer_ddb_dict: dict,
    ) -> None:
        new_address_data_dict.pop("datetime_created")
        response: dict = http_add_address_to_customer(
            event={
                "pathParameters": {"username": persisted_customer_ddb_dict["username"]},
                "body": json.dumps(new_address_data_dict),
            },
            context=None,
        )

        assert response
        fetched_address: dict = json.loads(response["body"])
        fetched_address.pop("id")
        fetched_address.pop("datetime_created")
        customer_email: str = fetched_address.pop("email")
        assert fetched_address == new_address_data_dict
        assert customer_email == persisted_customer_ddb_dict["email"]

    def test_add_address_to_customer_returns_404_with_bad_username(
        self,
        new_address_data_dict: dict,
    ) -> None:
        new_address_data_dict.pop("datetime_created")
        response: dict = http_add_address_to_customer(
            event={
                "pathParameters": {"username": "kif.kroker"},
                "body": json.dumps(new_address_data_dict),
            },
            context=None,
        )

        assert response
        assert response["statusCode"] == "404"
        assert response["body"] == '{"message": "Customer not found"}'


class TestHttpCreateOrder:
    def test_create_order_succeeds(
        self,
        new_order_parameters: dict,
        order_data_dict: dict,
    ) -> None:
        response: dict = http_create_order(
            event={"body": json.dumps(new_order_parameters)},
            context=None,
        )

        assert response["statusCode"] == "201"
        contents: dict = json.loads(response["body"])

        assert contents["customer_email"] == order_data_dict["customer_email"]
        assert contents["delivery_address"] == order_data_dict["delivery_address"]
        assert contents["item_count"] == order_data_dict["item_count"]
        assert contents["status"] == order_data_dict["status"]
        assert contents["status"] == OrderStatus.NEW

    def test_create_order_returns_422_on_invalid_address(
        self,
        new_order_parameters: dict,
    ) -> None:
        new_order_parameters["delivery_address_id"] = "doom_at_11"

        response: dict = http_create_order(
            event={"body": json.dumps(new_order_parameters)},
            context=None,
        )

        assert response["statusCode"] == "422"
        assert response["body"] == '{"message": "Invalid delivery_address_id"}'

    def test_create_order_returns_422_on_invalid_customer_email(
        self,
        new_order_parameters: dict,
    ) -> None:
        new_order_parameters[
            "customer_email"
        ] = "kif.kroker@decomcraticorderofplanets.com"

        response: dict = http_create_order(
            event={"body": json.dumps(new_order_parameters)},
            context=None,
        )

        assert response["statusCode"] == "422"
        assert response["body"] == '{"message": "Customer not found."}'


class TestHttpGetDomainOrder:
    def test_http_get_domain_order(
        self,
        persisted_order_ddb_dict: dict,
        persisted_line_item_ddb_dict: dict,
    ) -> None:
        response: dict = http_get_domain_order(
            event={
                "pathParameters": {
                    "order_id": persisted_order_ddb_dict["id"],
                }
            },
            context=None,
        )

        order_client: OrderService = OrderService()
        domain_order: Order = order_client.get_domain_order_by_id(
            persisted_order_ddb_dict["id"]
        )

        assert response["statusCode"] == "200"
        assert response["body"] == domain_order.json()


class TestHttpAddLineItem:
    def test_http_add_line_item_succeeds(
        self,
        persisted_order_ddb_dict: dict,
        line_item_data_dict: dict,
    ) -> None:
        new_line_item_data = deepcopy(line_item_data_dict)
        new_line_item_data.pop("id")
        new_line_item_data.pop("order_id")
        response: dict = http_add_line_item(
            event={
                "pathParameters": {
                    "order_id": persisted_order_ddb_dict["id"],
                },
                "body": json.dumps(new_line_item_data),
            },
            context=None,
        )

        assert response
        assert response["statusCode"] == "201"
        line_item: dict = json.loads(response["body"])

        key: dict = LineItemFactory.calculate_key(
            persisted_order_ddb_dict["id"],
            line_item["id"],
        )

        fetched_line_item: dict = get_item(key)
        assert fetched_line_item
