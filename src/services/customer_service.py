from datetime import datetime
from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from ksuid import ksuid

from src.dynamodb.helpers import put_item, query_by_key_condition_expression
from src.dynamodb.ModelFactory import AddressFactory, CustomerFactory
from src.models import Customer, DynamoAddress
from src.services.base_service import BaseService
from src.services.exceptions import (
    CreateCustomerException,
    CustomerLookupException,
    DuplicateCustomerKeyException,
)


class CustomerService(BaseService):
    FACTORY: CustomerFactory = CustomerFactory

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
    ) -> DynamoAddress:
        customer_items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key("sk").eq(
                f"{CustomerFactory.SK_ENTITY}#{username}"
            )
            & Key("pk").begins_with("Customer#"),
            index_name="sk_pk_index",
            table_name=self.TABLE_NAME,
        )

        if not customer_items:
            raise CustomerLookupException("Unable to locate Customer.")

        if len(customer_items) > 1:
            raise DuplicateCustomerKeyException

        customer: dict = customer_items[0]
        address_id: ksuid = ksuid()

        new_address_data["id"] = str(address_id)
        new_address_data["email"] = customer["email"]
        new_address_data["datetime_created"] = address_id.getDatetime().strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        address_factory: AddressFactory = AddressFactory(new_address_data)

        put_item(
            item=address_factory.item,
            table_name=self.TABLE_NAME,
        )

        return address_factory.model

    def get_customer_by_email(
        self,
        email: str,
    ) -> Customer:
        customer_items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key(f"{CustomerFactory.PK_ENTITY}#{email}")
            & Key("sk").begins_with(f"{CustomerFactory.SK_ENTITY}#"),
            table_name=self.TABLE_NAME,
        )

        if not customer_items:
            raise CustomerLookupException("Unable to locate Customer.")

        return CustomerFactory(customer_items[0]).model

    def get_customer_items_by_email(
        self,
        email: str,
    ) -> List[dict]:
        customer_items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key("pk").eq(
                f"{CustomerFactory.PK_ENTITY}#{email}"
            ),
            table_name=self.TABLE_NAME,
        )

        if not customer_items:
            raise CustomerLookupException("Unable to locate Customer.")

        return customer_items
