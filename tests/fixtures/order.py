from copy import deepcopy
from decimal import Decimal

import pytest
from ksuid import ksuid

from src.dynamodb.helpers import put_item
from src.dynamodb.ModelFactory import OrderFactory, LineItemFactory
from src.models import DynamoOrder


@pytest.fixture
def order_ddb_dict() -> dict:
    id_ksuid: ksuid = ksuid()
    pk_value: str = f"{OrderFactory.PK_ENTITY}#{str(id_ksuid)}"

    return {
        "pk": pk_value,
        "sk": pk_value,
        "id": str(id_ksuid),
        "entity": OrderFactory.PK_ENTITY,
        "customer_email": "zapp.brannigan@decomcraticorderofplanets.com",
        "delivery_address": {
            "line1": "471 1st Street Ct",
            "line2": None,
            "city": "Gotham",
            "state": "IL",
            "zipcode": "60603",
        },
        "datetime_created": id_ksuid.getDatetime().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "new",
        "item_count": Decimal("0"),
    }


@pytest.fixture
def order_data_dict(
    order_ddb_dict: dict,
) -> dict:
    order_data: dict = deepcopy(order_ddb_dict)
    order_data.pop("pk")
    order_data.pop("sk")
    order_data.pop("entity")

    return order_data


@pytest.fixture
def new_order_data_dict(
    order_data_dict: dict,
) -> dict:
    new_order_data = deepcopy(order_data_dict)
    new_order_data.pop("datetime_created")
    new_order_data.pop("id")

    return new_order_data


@pytest.fixture
def new_order_parameters(
    persisted_address_ddb_dict: dict,
    new_order_data_dict: dict,
) -> dict:
    parameter_data: dict = deepcopy(new_order_data_dict)
    parameter_data.pop("delivery_address")
    parameter_data.pop("status")
    parameter_data.pop("item_count")
    parameter_data["delivery_address_id"] = persisted_address_ddb_dict["id"]

    return parameter_data


@pytest.fixture
def persisted_order_ddb_dict(
    order_ddb_dict: dict,
) -> dict:
    put_item(order_ddb_dict)

    return order_ddb_dict


@pytest.fixture
def persisted_dynamo_order(
    persisted_order_ddb_dict: dict,
) -> DynamoOrder:
    return OrderFactory(persisted_order_ddb_dict).model


@pytest.fixture
def line_item_ddb_dict(
    order_ddb_dict: dict,
) -> dict:
    return {
        "pk": order_ddb_dict["pk"],
        "sk": f"{LineItemFactory.SK_ENTITY}#01",
        "entity": LineItemFactory.SK_ENTITY,
        "id": "01",
        "name": "Popplers",
        "description": "Omicronian enities of small proportions.",
        "quantity": Decimal("100"),
        "order_id": order_ddb_dict["id"],
    }


@pytest.fixture
def persisted_line_item_ddb_dict(line_item_ddb_dict: dict) -> dict:
    put_item(line_item_ddb_dict)
    return line_item_ddb_dict


@pytest.fixture
def line_item_data_dict(line_item_ddb_dict: dict) -> dict:
    line_item_data: dict = deepcopy(line_item_ddb_dict)
    line_item_data.pop("pk")
    line_item_data.pop("sk")
    line_item_data.pop("entity")

    return line_item_data
