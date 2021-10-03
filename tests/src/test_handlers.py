import pytest
import simplejson as json

from src.handlers import http_create_customer, http_create_order
from src.models.order import OrderStatus


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
        persisted_order_ddb_dict,
    ):
        pass
