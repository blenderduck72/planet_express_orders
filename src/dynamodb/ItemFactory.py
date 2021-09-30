import simplejson as json

from pydantic import BaseModel

from src.dynamodb.helpers import get_item, put_item


class DynamoItem:
    def __init__(
        self,
        MODEL: BaseModel or dict,
        PK_ENTITY: str,
        SK_ENTITY: str,
        PK_FIELD: str,
        SK_FIELD: str,
        **kwargs,
    ):
        if not MODEL or not PK_ENTITY or not PK_FIELD:
            raise Exception("PK_ENTITY and PK_FIELD are required")

        self.model: BaseModel or dict = MODEL
        self.pk_entity: str = PK_ENTITY
        self.sk_entity: str = SK_ENTITY
        self.pk_field: str = PK_FIELD
        self.sk_field: str = SK_FIELD

    @property
    def entity(self) -> str:
        if self.sk_entity:
            return self.sk_entity

        return self.pk_entity

    @property
    def pk(self) -> str:
        if not self.pk_entity or not self.pk_field:
            raise Exception("Model must have a PK_ENTIY & PK_FIELD set")

        if isinstance(self.model, BaseModel):
            return f"{self.pk_entity}#{getattr(self.model, self.pk_field)}"

        if isinstance(self.model, dict):
            return f"{self.pk_entity}#{self.model[self.pk_field]}"

        raise Exception("Model is not a valid Pydantic Model or Dictionary")

    @property
    def sk(self) -> str:
        if not self.sk_entity:
            return self.pk
        else:
            if isinstance(self.model, BaseModel):
                return f"{self.sk_entity}#{getattr(self.model, self.sk_field)}"

            if isinstance(self.model, dict):
                return f"{self.sk_entity}#{self.model[self.sk_field]}"

    @property
    def key(self) -> dict:
        return {
            "pk": self.pk,
            "sk": self.sk,
        }


class ItemFactory:
    PK_ENTITY: str = None
    SK_ENTITY: str = None
    PK_FIELD: str = None
    SK_FIELD: str = None
    BASE_MODEL: BaseModel = None

    @classmethod
    def create_item(cls, data: dict) -> BaseModel:
        pass

    @classmethod
    def update_item(cls, data: dict):
        pass

    @classmethod
    def save_item_from_model(
        cls,
        model: BaseModel,
    ) -> None:
        item: dict = cls.model_to_item(model, **cls.__dict__)

        put_item(item)

    @classmethod
    def save_item_from_dict(
        cls,
        data: dict,
    ) -> None:
        model: BaseModel = cls.BASE_MODEL(**data)
        cls.save_item_from_model(model)

    @classmethod
    def get_item_dict_by_model(
        cls,
        model: BaseModel,
    ) -> dict:
        dynamo_item: DynamoItem = DynamoItem(model, **cls.__dict__)
        item: dict = get_item(key=dynamo_item.key)

        return item

    @classmethod
    def item_to_model(cls, item: dict) -> BaseModel:
        return cls.BASE_MODEL(**item)

    @classmethod
    def model_to_item(
        cls,
        model: BaseModel,
        **kwargs,
    ) -> dict:
        dynamo_item: DynamoItem = DynamoItem(model, **cls.__dict__)
        serialized_model: dict = json.loads(model.json())

        serialized_model["pk"] = dynamo_item.pk
        serialized_model["sk"] = dynamo_item.sk
        serialized_model["entity"] = dynamo_item.entity

        return serialized_model

    @classmethod
    def get_item_by_key(
        cls,
        key: dict,
        model_class: BaseModel or None = None,
    ) -> BaseModel or None:
        item: dict = get_item(key)

        if not item:
            return None

        if model_class:
            return model_class(**item)

        return item

    @classmethod
    def get_model_key(
        cls,
        model: BaseModel,
    ) -> dict:
        dynamo_item: DynamoItem = DynamoItem(model, **cls.__dict__)
        return dynamo_item.key
