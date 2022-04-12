from functools import reduce
from typing import List

import boto3
from boto3.dynamodb.conditions import Attr, Equals, NotEquals, Or
from mypy_boto3_dynamodb.service_resource import _Table

from src.constants import TABLE_NAME

def get_item(
    key: dict,
    table_name: str = TABLE_NAME,
) -> dict or None:
    """
    Adds an Address to a Customer entity.

    Parameters:
        key (dict): Dictionary representation of DynamoDB key.
        table_name (str): DynamoDB table to perform get_item operation.

    Returns:
        item (dict): Pydantic DynamoAddress model.

    """
    table: _Table = boto3.resource("dynamodb").Table(table_name)
    return table.get_item(Key=key).get("Item")


def put_item(
    item: dict,
    table_name: str = TABLE_NAME,
) -> None:
    """
    Saves an Item to DynamoDB.

    Parameters:
        item (dict): Dictionary that item represents item to save.
        table_name (str): DynamoDB table to perform put_item operation.

    Returns:
        None

    """
    table: _Table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item=item)


def query_by_key_condition_expression(
    key_condition_expression: Equals,
    index_name: str = None,
    table_name: str = TABLE_NAME,
) -> List[dict]:
    """
    Retrieves a list of Dictionary that represents DynamoDB items.

    Parameters:
        key_condition_expression (Equals): DynamoDB Condition utilized for query.
        index_name (str) : Name of index to query
        table_name (str): DynamoDB table to perform query operation.

    Returns:
        None

    """
    table: _Table = boto3.resource("dynamodb").Table(table_name)

    options: dict = {
        "KeyConditionExpression": key_condition_expression,
    }
    if index_name:
        options["IndexName"] = index_name

    return table.query(**options).get("Items", [])
