from datetime import datetime
from typing import List

import boto3
from boto3.dynamodb.conditions import Key

from dynamodb.helpers import query_by_key_condition_expression
from src.models.address import Address, DynamoAddress
from src.models.customer import Customer
from src.services.base_service import BaseService
from src.dynamodb.ModelFactory import CustomerFactory
from src.services.exceptions import CreateCustomerException


class CustomerService(BaseService):
    def create_customer(
        self,
        new_customer_data: dict,
    ) -> Customer:
        """
        Accepts a new Customer payload and creates a new
        customer if the username is not already in use.

        Parameters:
            new_customer_data: dict
        Returns:
            customer(Customer): Pydantic Customer model
        """

        new_customer_data["date_created"] = datetime.now().date().isoformat()

        customer_factory: CustomerFactory = CustomerFactory(new_customer_data)

        client = boto3.resource("dynamodb")
        table = client.Table(self.TABLE_NAME)

        try:
            table.put_item(
                Item=customer_factory.item,
                ConditionExpression="attribute_not_exists(#username)",
                ExpressionAttributeNames={
                    "#username": "username",
                },
            )

        except client.meta.client.exceptions.ConditionalCheckFailedException:
            raise CreateCustomerException("Account already exists")

        return customer_factory.model

    def add_customer_address(
        self,
        username: str,
        new_address_data: dict,
    ) -> Address:
        customers: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key("sk").eq(
                f"{CustomerFactory.SK_ENTITY}#{username}"
            ),
            index_name="sk_pk_index",
            table_name=self.TABLE_NAME,
        )
