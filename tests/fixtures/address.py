from datetime import datetime
from copy import deepcopy

import pytest
from ksuid import ksuid

from src.dynamodb.helpers import put_item
from src.dynamodb.ModelFactory import AddressFactory
from src.models import AddressType


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
