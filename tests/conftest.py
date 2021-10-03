from copy import deepcopy
from datetime import datetime
from decimal import Decimal


import boto3
import moto
import pytest
from ksuid import ksuid

from src.constants import TABLE_NAME
from src.dynamodb.helpers import put_item
from src.dynamodb.ModelFactory import (
    AddressFactory,
    CustomerFactory,
    LineItemFactory,
    OrderFactory,
)
from src.models.address import AddressType
from src.models.order import DynamoOrder


@pytest.fixture(scope="session")
def secret_key():
    return "secret"


@pytest.fixture(scope="function", autouse=True)
def mock_aws_table():
    with moto.mock_dynamodb2():
        boto3.client("dynamodb").create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "sk_pk_index",
                    "Projection": {"ProjectionType": "ALL"},
                    "KeySchema": [
                        {"AttributeName": "sk", "KeyType": "HASH"},
                        {"AttributeName": "pk", "KeyType": "RANGE"},
                    ],
                }
            ],
        )
        yield


@pytest.fixture
def address_ddb_dict(customer_ddb_dict) -> dict:

    address_id: ksuid = ksuid()
    return {
        "pk": f"{AddressFactory.PK_ENTITY}#{customer_ddb_dict['email']}",
        "sk": f"{AddressFactory.SK_ENTITY}#{str(address_id)}",
        "entity": AddressFactory.PK_ENTITY,
        "id": str(address_id),
        "line1": "471 1st Street Ct",
        "line2": None,
        "city": "Gotham",
        "state": "IL",
        "zipcode": "60603",
        "type": AddressType.DELIVERY,
        "datetime_created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


@pytest.fixture
def persisted_address_ddb_dict(address_ddb_dict) -> None:
    put_item(address_ddb_dict)
    return address_ddb_dict


@pytest.fixture
def address_data_dict(
    address_ddb_dict: dict,
) -> dict:
    address_data: dict = deepcopy(address_ddb_dict)
    address_data.pop("pk")
    address_data.pop("sk")
    address_data.pop("entity")

    return address_data


@pytest.fixture
def new_address_data_dict(
    address_data_dict: dict,
) -> dict:
    new_address_data: dict = deepcopy(address_data_dict)
    new_address_data.pop("id")

    return new_address_data


@pytest.fixture
def customer_ddb_dict() -> dict:
    return {
        "pk": f"{CustomerFactory.PK_ENTITY}#zapp.brannigan@decomcraticorderofplanets.com",
        "sk": f"{CustomerFactory.SK_ENTITY}#VelourFog",
        "first_name": "Zapp",
        "last_name": "Brannigan",
        "email": "zapp.brannigan@decomcraticorderofplanets.com",
        "username": "VelourFog",
        "entity": CustomerFactory.SK_ENTITY,
        "date_created": datetime.now().date().isoformat(),
    }


@pytest.fixture
def persisted_customer_ddb_dict(
    customer_ddb_dict: dict,
) -> dict:
    put_item(customer_ddb_dict)

    return customer_ddb_dict


@pytest.fixture
def customer_data_dict(customer_ddb_dict: dict) -> dict:
    customer_data: dict = deepcopy(customer_ddb_dict)
    customer_data.pop("pk")
    customer_data.pop("sk")
    customer_data.pop("entity")

    return customer_data


@pytest.fixture
def new_customer_data_dict(customer_data_dict: dict) -> dict:
    new_customer_data: dict = deepcopy(customer_data_dict)
    new_customer_data.pop("date_created")

    return new_customer_data


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
