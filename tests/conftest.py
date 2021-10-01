from copy import deepcopy
from decimal import Decimal

import boto3
import moto
import pytest
from ksuid import ksuid

from src.constants import TABLE_NAME
from src.dynamodb.helpers import put_item
from src.dynamodb.ModelFactory import CustomerFactory, LineItemFactory, OrderFactory
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
        )
        yield


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
        "date_created": "2021-05-04",
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
def order_data_dict(order_ddb_dict: dict) -> dict:
    order_data: dict = deepcopy(order_ddb_dict)
    order_data.pop("pk")
    order_data.pop("sk")
    order_data.pop("entity")

    return order_data


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
