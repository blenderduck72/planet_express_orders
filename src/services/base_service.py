from src.constants import TABLE_NAME
from src.factory.item_factory import ItemFactory
from src.dynamodb.helpers import get_item


class BaseService:
    """
    Generic Service that other services can inhert.

    ...

    Attributes
    ----------
    FACTORY : CustomerFactory
        ItemFactory used by obtain root Model's Key
    TABLE_NAME: str
        DynamoDB Table Name utilized by service.


    Methods
    -------
    get_factory_item_by_key(key: dict) -> ItemFactory
        Retrieves a specific DynamoDB item and returns it
        wrapped in an ItemFactory


    """

    TABLE_NAME = TABLE_NAME
    FACTORY: ItemFactory

    def get_factory_item_by_key(
        self,
        key: dict,
    ) -> ItemFactory or None:
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

        return self.FACTORY(item)
