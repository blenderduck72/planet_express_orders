from functools import reduce
from typing import List

import boto3
from boto3.dynamodb.conditions import And, Attr, Equals, Key, NotEquals, Or

from src.constants import TABLE_NAME


def get_item(
    key: dict,
    table_name: str = TABLE_NAME,
) -> dict or None:
    table = boto3.resource("dynamodb").Table(table_name)
    return table.get_item(Key=key).get("Item")


def update_item_attributes_if_changed(
    key: dict,
    item_attributes: dict,
    table_name: str = TABLE_NAME,
) -> dict:
    client = boto3.resource()
    table = client.Table(table_name)
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


def put_item(
    item: dict,
    table_name: str = TABLE_NAME,
) -> None:
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item=item)


def get_items_by_query(
    key: dict,
    index_name: str = None,
    table_name: str = TABLE_NAME,
) -> List[dict]:

    table = boto3.resource("dynamodb").Table(table_name)
    key_condition_expression = And(*[Key(k).eq(v) for k, v in key.items()])
    options: dict = {"KeyConditionExpression": key_condition_expression}

    if index_name:
        options["IndexName"] = index_name

    return table.query(**options).get("Items", [])


def query_by_key_condition_expression(
    key_condition_expression: Equals,
    index_name: str = None,
    table_name: str = TABLE_NAME,
) -> List[dict]:
    table = boto3.resource("dynamodb").Table(table_name)

    options: dict = {
        "KeyConditionExpression": key_condition_expression,
    }
    if index_name:
        options["IndexName"] = index_name

    return table.query(**options).get("Items", [])
