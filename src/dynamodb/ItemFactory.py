from typing import List
from copy import deepcopy

import simplejson as json
from boto3.dynamodb.conditions import Key

from pydantic import BaseModel

from src.dynamodb.helpers import (
    get_item,
    put_item,
    query_by_key_condition_expression,
    update_item_attributes_if_changed,
)


class ItemFactory:
    PK_ENTITY: str
    SK_ENTITY: str
    PK_FIELD: str
    SK_FIELD: str

    def __init__(
        self,
        model: BaseModel or dict,
    ):
        self.model: BaseModel or dict = model

    @property
    def entity(self) -> str:
        if self.SK_ENTITY:
            return self.SK_ENTITY

        return self.PK_ENTITY

    @property
    def pk(self) -> str:
        if not self.PK_ENTITY or not self.PK_FIELD:
            raise Exception("Model must have a PK_ENTIY & PK_FIELD set")

        if isinstance(self.model, BaseModel):
            return f"{self.PK_ENTITY}#{getattr(self.model, self.PK_FIELD)}"

        if isinstance(self.model, dict):
            return f"{self.PK_ENTITY}#{self.model[self.PK_FIELD]}"

        raise Exception("Model is not a valid Pydantic Model or Dictionary")

    @property
    def sk(self) -> str:
        if not self.SK_ENTITY:
            return self.pk
        else:
            if isinstance(self.model, BaseModel):
                return f"{self.SK_ENTITY}#{getattr(self.model, self.SK_FIELD)}"

            if isinstance(self.model, dict):
                return f"{self.SK_ENTITY}#{self.model[self.SK_FIELD]}"

    @property
    def key(self) -> dict:
        return {
            "pk": self.pk,
            "sk": self.sk,
        }

    @property
    def item(self):
        if isinstance(self.model, BaseModel):
            item: dict = json.loads(self.model.json())

        elif isinstance(self.model, dict):
            item: dict = deepcopy(self.model)

        if not item:
            raise Exception

        item["pk"] = self.pk
        item["sk"] = self.sk
        item["entity"] = self.entity

        return item


# class ItemFactory:
#     PK_ENTITY: str = None
#     SK_ENTITY: str = None
#     PK_FIELD: str = None
#     SK_FIELD: str = None
#     DDB_MODEL: BaseModel = None
#     DOMAIN_MODEL: BaseModel = None

#     @classmethod
#     def create_item(cls, data: dict) -> BaseModel:
#         item: dict = cls.save_item_from_dict(data)
#         return cls.DDB_MODEL(**item)

#     @classmethod
#     def get_domain_item(
#         cls,
#         pk_value: str,
#     ) -> List[dict] or BaseModel:
#         aggregate: List[dict] = query_by_key_condition_expression(
#             Key("pk").eq(pk_value)
#         )

#         return aggregate

#     @classmethod
#     def update_item(cls, data: dict) -> None:
#         update_item_attributes_if_changed(data)

#     @classmethod
#     def save_item_from_model(
#         cls,
#         model: BaseModel,
#     ) -> dict:
#         item: dict = cls.model_to_item(model, **cls.__dict__)
#         put_item(item)

#         return item

#     @classmethod
#     def save_item_from_dict(
#         cls,
#         data: dict,
#     ) -> dict:
#         model: BaseModel = cls.DDB_MODEL(**data)
#         item: dict = cls.save_item_from_model(model)

#         return item

#     @classmethod
#     def get_item_dict_by_model(
#         cls,
#         model: BaseModel,
#     ) -> dict:
#         dynamo_item: DynamoItem = DynamoItem(model, **cls.__dict__)
#         item: dict = get_item(key=dynamo_item.key)

#         return item

#     @classmethod
#     def item_to_model(cls, item: dict) -> BaseModel:
#         return cls.DDB_MODEL(**item)

#     @classmethod
#     def model_to_item(
#         cls,
#         model: BaseModel,
#         **kwargs,
#     ) -> dict:
#         dynamo_item: DynamoItem = DynamoItem(model, **cls.__dict__)
#         serialized_model: dict = json.loads(model.json())

#         serialized_model["pk"] = dynamo_item.pk
#         serialized_model["sk"] = dynamo_item.sk
#         serialized_model["entity"] = dynamo_item.entity

#         return serialized_model

#     @classmethod
#     def get_item_by_key(
#         cls,
#         key: dict,
#         model_class: BaseModel or None = None,
#     ) -> BaseModel or None:
#         item: dict = get_item(key)

#         if not item:
#             return None

#         if model_class:
#             return model_class(**item)

#         return item

#     @classmethod
#     def get_model_key(
#         cls,
#         model: BaseModel,
#     ) -> dict:
#         dynamo_item: DynamoItem = DynamoItem(model, **cls.__dict__)
#         return dynamo_item.key
