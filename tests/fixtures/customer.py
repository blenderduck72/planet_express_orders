from datetime import datetime
from copy import deepcopy

import pytest

from src.dynamodb.ModelFactory import CustomerFactory
from src.dynamodb.helpers import put_item


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
