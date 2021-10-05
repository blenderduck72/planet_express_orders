# DynamoDB Single Table Design w/Planet Express Orders
Provides an example project of utilizing Single Dynamodb Table Design.


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
This can be accomplished because they share the same `pk` value. Between these two entities the `sk` value is what makes them unique. This is allowed to happen because a composity key was defined when the table was created:
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

## TransactItems / Handling Business Logic
