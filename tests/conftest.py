import boto3
import moto
import pytest

from src.constants import TABLE_NAME
from tests.fixtures import *


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
