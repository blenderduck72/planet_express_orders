from datetime import datetime
from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from ksuid import ksuid
from mypy_boto3_dynamodb.service_resource import _Table

from src.dynamodb.helpers import put_item, query_by_key_condition_expression
from src.models import Customer, DynamoAddress
from src.services.base_service import BaseService
from src.services.exceptions import (
    CreateCustomerException,
    CustomerLookupException,
    DuplicateCustomerKeyException,
)


class CustomerService(BaseService):
    """
    Represents Customer Service.

    ...

    Attributes
    ----------
    TABLE_NAME: str
        DynamoDB Table Name utilized by service.


    Methods
    -------
    get_item_by_key(key: dict, model: DynamoItem) -> DynamoItem
        Retrieves a specific DynamoDB item and returns a
        instantiated DynamoItem

    create_customer(new_customer_data: dict)
        Saves a new customer to DynamoDB

    add_Customer_address(username: str, new_address_data)
        Adds an Address to a Customer.

    get_customer_by_email(email: str)
        Retrieves a Customer by email.

    get_customer_items_by_email(email: str)
        Retrieves a list of Customer and Address entities
        as dictionaries associated with the email.

    """

    def add_customer_address(
        self,
        username: str,
        new_address_data: dict,
    ) -> DynamoAddress:
        """
        Adds an Address to a Customer entity.

        Parameters:
            username (str): username of the Customer.
            new_address_data(dict): Dictionary of address data (NewAddresssSchema).

        Returns:
            dynamo_address (DynamoAddress): Pydantic DynamoAddress model.

        Rasies:
            CustomerLookupException (Exception): Occurs if username is not saved in DynamoDB
            DuplicateCustomerKeyException (Exception): Occurs if there are multiple of the same username.
        """
        customer_items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key("sk").eq(f"{Customer._SK_ENTITY}#{username}")
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
        address: DynamoAddress = DynamoAddress(**new_address_data)

        put_item(
            item=address.item,
            table_name=self.TABLE_NAME,
        )

        return address

    def create_customer(
        self,
        new_customer_data: dict,
    ) -> Customer:
        """
        Accepts a new Customer payload and creates a new
        customer if the username is not already in use.

        Parameters:
            new_customer_data (dict): Dictionary of customer data (NewCustomerSchema).

        Returns:
            customer (Customer): Pydantic Customer model
        """
        new_customer_data["date_created"] = datetime.now().date().isoformat()
        customer: Customer = Customer(**new_customer_data)
        client: _Table = boto3.resource("dynamodb")
        table: _Table = client.Table(self.TABLE_NAME)
        try:
            table.put_item(
                Item=customer.item,
                ConditionExpression="attribute_not_exists(#username)",
                ExpressionAttributeNames={
                    "#username": "username",
                },
            )

        except client.meta.client.exceptions.ConditionalCheckFailedException:
            raise CreateCustomerException("Account already exists")

        return customer

    def get_customer_by_email(
        self,
        email: str,
    ) -> Customer:
        """
        Returns a Customer Model by emai.

        Parameters:
            email (str): email of the Customer.

        Returns:
            customer (Customer): Pydantic DynamoAddress model.

        Rasies:
            CustomerLookupException (Exception): Occurs if username is not saved in DynamoDB
        """
        customer_items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key(f"{Customer._PK_ENTITY}#{email}")
            & Key("sk").begins_with(f"{Customer._SK_ENTITY}#"),
            table_name=self.TABLE_NAME,
        )

        if not customer_items:
            raise CustomerLookupException("Unable to locate Customer.")

        return Customer(**customer_items[0])

    def get_customer_items_by_email(
        self,
        email: str,
    ) -> List[dict]:
        """
        Returns a list of Customer and Address dictionary items by email.

        Parameters:
            email (str): email of the Customer.

        Returns:
            customer_items (List[dict]): List of Customer and Address Dictionaries.

        Rasies:
            CustomerLookupException (Exception): Occurs if username is not saved in DynamoDB
        """
        customer_items: List[dict] = query_by_key_condition_expression(
            key_condition_expression=Key("pk").eq(f"{Customer._PK_ENTITY}#{email}"),
            table_name=self.TABLE_NAME,
        )

        if not customer_items:
            raise CustomerLookupException("Unable to locate Customer.")

        return customer_items
