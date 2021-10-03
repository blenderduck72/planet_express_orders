from _pytest.nodes import Item
from src.constants import TABLE_NAME
from src.dynamodb.ItemFactory import ItemFactory
from src.dynamodb.helpers import get_item


class BaseService:
    TABLE_NAME = TABLE_NAME
    FACTORY: ItemFactory

    def get_factory_item_by_key(self, key: dict) -> ItemFactory or None:
        item: dict = get_item(key=key, table_name=self.TABLE_NAME)

        if not item:
            return None

        return self.FACTORY(item)
