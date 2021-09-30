from functools import reduce
from typing import List

import boto3
from boto3.dynamodb.conditions import And, Attr, Equals, Key, NotEquals, Or

from src.constants import TABLE_NAME


def get_item(key: dict) -> dict or None:
    table = boto3.resource("dynamodb").Table(TABLE_NAME)
    return table.get_item(Key=key).get("Item")


def update_item_attributes_if_changed(
    key: dict,
    item_attributes: dict,
) -> dict:
    client = boto3.resource()
    table = client.Table(TABLE_NAME)
    conditions: List[NotEquals] = [
        Attr(key).ne(value) for key, value in item_attributes.items()
    ]
    condition_expression = (
        reduce(Or, conditions) if len(conditions) > 1 else conditions[0]
    )

    return table.update_item(
        Key=key,
        UpdateExpression=f'SET {",".join([f"#{key} =:{key}" for key in item_attributes.keys()])}',
        ExpressionAttributeNames={f"#{key}": key for key in item_attributes.keys()},
        ExpressionAttributeValues={
            f":{key}": value for key, value in item_attributes.items()
        },
        ConditionExpression=condition_expression,
    )


def put_item(item: dict) -> None:
    table = boto3.resource("dynamodb").Table(TABLE_NAME)
    table.put_item(Item=item)


def get_items_by_query(
    key: dict,
    index_name: str = None,
) -> List[dict]:

    table = boto3.resource("dynamodb").Table(TABLE_NAME)
    key_condition_expression = And(*[Key(k).eq(v) for k, v in key.items()])
    options: dict = {"KeyConditionExpression": key_condition_expression}

    if index_name:
        options["IndexName"] = index_name

    return table.query(**options).get("Items", [])


def query_by_key_condition_expression(
    key_condition_expression: Equals, index_name: str = None
) -> List[dict]:
    table = boto3.resource("dynamodb").Table(TABLE_NAME)

    options: dict = {
        "KeyConditionExpression": key_condition_expression,
    }
    if index_name:
        options["IndexName"] = index_name

    return table.query(**options).get("Items", [])
