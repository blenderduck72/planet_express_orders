from src.constants import TABLE_NAME
from src.dynamodb.helpers import get_item
from src.models.base_model import DynamoItem


class BaseService:
    """
    Generic Service that other services can inhert.

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
    """

    TABLE_NAME = TABLE_NAME

    def get_item_by_key(
        self,
        key: dict,
        model: DynamoItem,
    ) -> DynamoItem or None:
        """
        Accepts dictionary that describes a DynamoDB key and
        returns its corresponding item wrapped in an ItemFactory.

        Parameters:
            key (dict): Dictionary of Dynamodb key. {'pk':'value, 'sk': 'value'}

        Returns:
            item_factory (ItemFactory): Pydantic Customer model
        """
        item: dict = get_item(key=key, table_name=self.TABLE_NAME)

        if not item:
            return None

        return model(**item)
