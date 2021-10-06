from functools import reduce
from typing import List

import boto3
from boto3.dynamodb.conditions import And, Attr, Equals, Key, NotEquals, Or

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
    table = boto3.resource("dynamodb").Table(table_name)
    return table.get_item(Key=key).get("Item")


def update_item_attributes_if_changed(
    key: dict,
    item_attributes: dict,
    table_name: str = TABLE_NAME,
) -> dict:
    """
    Updates any changed attributes on an item if present.

    Parameters:
        key (dict): Dictionary representation of DynamoDB key.
        item_attributes (dict): Dictionary of attributes to update.
        table_name (str): DynamoDB table to perform update_item operation.

    Returns:
        item (dict): Pydantic DynamoAddress model.
        none (None): Returned if key is not tied to saved item.

    """
    client = boto3.resource()
    table = client.Table(table_name)
    conditions: List[NotEquals] = [
        Attr(key).ne(value) for key, value in item_attributes.items()
    ]
    condition_expression = (
        reduce(Or, conditions) if len(conditions) > 1 else conditions[0]
    )

    try:
        table.update_item(
            Key=key,
            UpdateExpression=f'SET {",".join([f"#{key} =:{key}" for key in item_attributes.keys()])}',
            ExpressionAttributeNames={f"#{key}": key for key in item_attributes.keys()},
            ExpressionAttributeValues={
                f":{key}": value for key, value in item_attributes.items()
            },
            ConditionExpression=condition_expression,
        )
    except client.meta.client.exceptions.ConditionalCheckFailedException:
        pass


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
    table = boto3.resource("dynamodb").Table(table_name)
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
    table = boto3.resource("dynamodb").Table(table_name)

    options: dict = {
        "KeyConditionExpression": key_condition_expression,
    }
    if index_name:
        options["IndexName"] = index_name

    return table.query(**options).get("Items", [])
