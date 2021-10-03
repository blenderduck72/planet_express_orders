import pytest
import simplejson as json

from src.handlers import http_create_customer


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
