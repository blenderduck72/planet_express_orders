# DynamoDB Single Table Design w/Planet Express Orders
Provides an example project of utilizing Single Dynamodb Table Design.

# Table Of Contents
- [How to try out the project](#how-to-try-out-the-project)
- [How to remove](#how-to-remove)
- [Single Table Design Concepts](#single-table-design-concepts)
    - [1 Query 2 or more Entities](#1-query-2-or-more-entities)
    - [Advanced Queries: Part 1](#advanced-queries-part-1)
    - [Advanced Queries: Part 2](#advanced-queries-part-2)
    - [Advanced Queries: Part 3](#advanced-queries-part-3)
    - [AutoIncrement](#autoincrement)
        - [Increment a key](#increment-a-key)
        - [De-increment a key](#de-increment-a-key)
    - [Handling Business Logic with ConditionExpressions](#handling-business-logic-with-conditionexpressions)
    - [Handling Uniqueness](#handling-uniqueness)
- [Recommended Reading](#recommended-reading)


# How to try out the project
- Install serverless
- Modify the serverless.yml file as seen fit
- Run 
```
pipenv install
pipenv install --dev
```
- serverless deploy

## How to remove
- run 
```
serverless remove
```
## How to run the scripts included
The project includes a few scripts:
- [create_example_customer](scripts/create_example_customer.py)
- [create_order_example](scripts/create_example_order.py)
- [get_order_example](scripts/get_example_order.py)
- [add_line_item_example](scripts/add_line_item_to_order.py)
- [update_model_json](scripts/update_model_json.py)

They all utilize python [click](https://click.palletsprojects.com/en/8.0.x/).
To utilzie the scripts create a `.env` file in the root directory and add the following parameters:
```bash
CREATE_CUSTOMER_URL=""
CREATE_ORDER_URL=""
X_API_KEY=""
```
Fill in the order & customer urls, and the x-api-key that are retrieved from running
```
serverless deploy
```
To kick off a script simply run:
```bash
pipenv run python <scriptpath>
```
For example:
```bash
pipenv run python scripts/create_example_customer.py
```

I'd recommend the scripts be ran in the order listed above to populate the deployed DynamoDB table with examples.

The `get_order_example` and `add_line_item_example` require that an `--order_id` parameter be passed.


# Single Table Design Concepts:

## Disclaimer
DynamoDB is unique. Some of its concepts may seem counter intuitive, an anti-pattern, and reptitve, or duplicative. But it trades what may smell in favor of scalable performance.

## 1 Query 2 or more Entities
One of the more complicated aspects of DynamoDB is retrieving more than one entity in a query. This is difficult because DynamoDB does not support joins.

However, when utilizing Single Table Design, multiple and different entity types can be retrieved in a query, as long as the data is properly organized to allow for this.

The simplist example of this is a Parent/Child or One-To-Many relationship. Assume two records are in dyanmodb, one for an order:

```json
{
 "pk": "Order#0de9302cfae9a312bfefa4f542d41c04e03ee455",
 "sk": "Order#0de9302cfae9a312bfefa4f542d41c04e03ee455",
 "entity": "Order",
 "status": "new",
 "customer_email": "philipfry@planetexpress.com",
 "item_count": 0,
 "id": "0de9302cfae9a312bfefa4f542d41c04e03ee455",
 "datetime_created": "2021-10-04T00:00:00+00:00",
 "delivery_address": {
  "zipcode": "60603",
  "state": "IL",
  "line2": null,
  "city": "Gotham",
  "line1": "471 1st Street Ct"
 }
}
```
and one for a line_item:
```json
{
 "pk": "Order#0de9302cfae9a312bfefa4f542d41c04e03ee455",
 "sk": "LineItem#01",
 "quantity": 100,
 "entity": "LineItem",
 "order_id": "0de9302cfae9a312bfefa4f542d41c04e03ee455",
 "description": "Omicronian enities of small proportions.",
 "id": "01",
 "name": "Popplers"
}
```
Though seperate entities, that can be be obtained via one query:
```python

table = boto3.resource('dynamodb').Table('table_name')
table.query(KeyConditionExpression=Key('pk').eq('Order#0de9302cfae9a312bfefa4f542d41c04e03ee455'))
```
This can be accomplished because they share the same `pk` value. Between these two entities the `sk` value is what makes them unique (yes the `order`'s pk and sk value are the same, this is by design). This is allowed to happen because a composity key was defined when the table was created:
```yaml
    PlanetExpressDB:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:custom.table_name}
        KeySchema:
          - AttributeName: pk
            KeyType: HASH
          - AttributeName: sk
            KeyType: RANGE
        AttributeDefinitions:
          - AttributeName: pk
            AttributeType: S
          - AttributeName: sk
            AttributeType: S
```
What can be retrieved by querying the partition key of a composite key introduces an important part of DynamoDB, DomainDrivenDesign, and Microservices: the [Aggregate](https://microservices.io/patterns/data/aggregate.html). In real life multiple entities may make an `order`; for example, `customer`, `recipient`, `address`, `line_item`, `billing`, etc. An `order` would be a composite of all these entities. An example of this in the current project is when a [Domain Order](src/services/order_service.py#L106)

To get a specific `line_item` or `order` the boto3's `get_item` method can still be used. Or a list of a specific items that creates an `order` can be retrieved by an updated query. If we wanted to retrieve just an `order`'s `line_items` we could update our `KeyConditionExpression` to:
```python
Key('pk').eq('Order#0de9302cfae9a312bfefa4f542d41c04e03ee455') & Key('sk').begins_with('LineItem#')
```
By having the partition key and sort key values be composed of an entity & and an id it allows for more flexible DynamoDB queries. 


## Advanced Queries: Part 1
More advanced queries may involve the use of a Global Secondary Index(GSI). At first glance a common patten would be to setup a GSI on a specific field, such as `status` to get all orders in a certain status. That GSI may also include a sort key of `datetime` submitted. 

Though this works, it can be limiting. 

One of the important aspects of a partition key and sort key in our earlier example was that they had the following pattern `entity#id`. Adding additional attributes that follow this pattern and utilizing them for a GSI allows for better queries.

## Advanced Queries: Part 2
This will note be elaborated on greatly, but advanced scalable queries involve composite sort keys.

Assume we had a service that was a collection of digital address books. As the service would be composed of several address books, a book may be our parent or partition key. To narrow our search to a specific area of one address book, using a composition sort key would be the answer.

```python
Key('pk').eq('The Greater Address Book of America') & Key('sk').begins_with('IL#MOLINE#61201')
```

## Advanced Queries: Part 3
To allow for advanced queries, sometimes data has to be duplicated across records and attributes. 

## AutoIncrement

### Key Incrementation

One of the first drawback with DynamoDB that many people discover is the lack of an auto incrementing key. Generally this may lead to the use UUIDs.

DynamoDB does allow for a pattern of secondary keys being incremented (so not the Parent or Partition Key - pk).

In this example assume that we want our `order`'s `line_items` id field to be auto-incremented when a `line_item` is added to an order and de-incremented when a `line_item` is removed. 

### Increment a key

To allow this to work the `order` would need a `item_count` attribute.

Before saving a `line_item` we would increment the `item_count` using an update expression. We would then retrieve the `item_count` value and utilize it create the `id` and `sk` value for the `line_item`.

The `order` update may look like:
```python
import boto3

table = boto3.resource("dynamodb").Table(self.TABLE_NAME)
response: dict = table.update_item(
    Key={
        "pk":"Order#0de9302cfae9a312bfefa4f542d41c04e03ee455", 
        "sk":"Order#0de9302cfae9a312bfefa4f542d41c04e03ee455",}
    },
    UpdateExpression="SET #item_count = #item_count + :incr",
    ExpressionAttributeNames={"#item_count": "item_count"},
    ExpressionAttributeValues={":incr": 1},
    ReturnValues="UPDATED_NEW",
)
```
The code right after this that would save the `line_item` may look like:
```python
item_count: Decimal = response["Attributes"]["item_count"]
new_line_item_data["pk"] = "Order#0de9302cfae9a312bfefa4f542d41c04e03ee455"
new_line_item_data["id"] = str(item_count).zfill(2) #01 looks nicer and is more sortable than just 1
new_line_item_data["sk"] = f"LineItem#{new_line_item_data['id']}"
new_line_item_data["order_id"] new_line_item_data["pk"].replace(
    "Order#", ""
)
table.put_item(Item=new_line_item_data)
```
Though this technique may raise some questions this is the standard technique for this practice. An example of this in the codebase can be found [here](src/services/order_service.py#L132)

### De-increment a key
Oddly, the technique for subtracting from `item_count` when a `line_item` feels more practical.

This can be done with boto3's [transact_write_items](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.transact_write_items) method. 

Sadly boto3 does not have this method directly on a `resource` item, which means to not deal with DynamoDB typed json the code may access the transact_write_items method through some different means.
```python
import boto3

client = boto3.resource("dynamodb").Table("planet_express_table")
client.meta.client.transact_write_items(
    TransactItems=[
        {
            "Update": {
                "TableName": "planet_express_table",
                "Key":{
                    "pk":"Order#0de9302cfae9a312bfefa4f542d41c04e03ee455", 
                    "sk":"Order#0de9302cfae9a312bfefa4f542d41c04e03ee455",}
                },
                "UpdateExpression": "SET #item_count = #item_count - :inc", # subtracts from item_count
                "ExpressionAttributeNames": {
                    "#item_count": "item_count",
                    "#status": "status",
                },
                "ExpressionAttributeValues": {
                    ":inc": 1,
                    ":new": "new",
                },
                "ConditionExpression": "#status IN (:new)", # ensures non-new orders can not have line_items removed.
            },
        },
        {
            "Delete": {
                "TableName": "planet_express_table",
                "Key": {
                    "pk":"Order#0de9302cfae9a312bfefa4f542d41c04e03ee455", 
                    "sk":"LineItem#01",}
                },
                "ConditionExpression": "attribute_exists(sk)", # ensures the line_item exists 
            },
        },
    ],
)
```
By bundling up the Delete and Update expression in the `transact_write_items` method we ensure that if one item fails due to a condition check not changes are made to any item. If one failes they all fail.

An example of this can be found [here](src/services/order_service.py#L154).

## Handling Business Logic with ConditionExpressions
As seen with the De-increment a key example, ConditionExpressions are a strong tool for adding, implementing, or enforcing Business Logic to the saving or updating of certain attributes. 

ConditionExpressions are a powerful tool that can: prevent something from saving if a value of an attribute is not in a list; can check whether something exists, can determine if value is of a certain type. 

Utilizing Single Table Design and ConditionExpressions handling Uniqueness can be accomplished.

## Handling Uniqueness
Assume that we have do not want to create a customer that already exists in our service, and that each customer in our service has a unique `username`

We can prevent overwriting or adding a new customer if there is an exising `username` utilizing dynamodb's ConditionExpression and the `attribute_not_exists` method.

```python
table = boto3.resource("dynamodb").Table("table_name")
table.put_item(
    Item={
        "pk": "Customer#philipfry@planetexpress.com",
        "sk": "User#pfry",
        "entity": "User",
        "last_name": "fry",
        "first_name": "philip",
        "username": "pfry",
        "date_created": "2021-10-04",
        "email": "philipfry@planetexpress.com"
    },
    ConditionExpression="attribute_not_exists(#username)",
    ExpressionAttributeNames={
        "#username": "username",
    },
)
```
If the following customer was already saved in DynamoDB when this operation is performed, boto3 would raise a `ConditionalCheckFailedException`.

An example of this in practice can be found [here](src/services/customer_service.py#L22).

# Recommended Reading
- The Alex Debrie Collection:
    - [Single Table Design](https://www.alexdebrie.com/posts/dynamodb-single-table/)
    - [TransactItems](https://www.alexdebrie.com/posts/dynamodb-transactions/)
    - [Light Partition Reading](https://www.alexdebrie.com/posts/dynamodb-partitions/)
    - [The Movie](https://www.youtube.com/watch?v=BnDKD_Zv0og)
    - [The book the movie was based off](https://www.dynamodbbook.com/)
    - [The live performance](https://www.youtube.com/watch?v=DIQVJqiSUkE)
- The AWS collection
    - [Adjacency List Design Pattern](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-adjacency-graphs.html)
    - [Composite Sort Keys](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html)
    - [ConditionExpression helpers](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.OperatorsAndFunctions.html)