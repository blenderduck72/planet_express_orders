import simplejson as json

from pydantic import BaseModel


class ItemFactory:
    PK_ENTITY: str
    SK_ENTITY: str
    PK_FIELD: str
    SK_FIELD: str
    DDB_MODEL: BaseModel
    DOMAIN_MODEL: BaseModel

    def __init__(
        self,
        data: dict,
    ):
        self.model = self.DDB_MODEL(**data)

    @property
    def entity(self) -> str:
        if self.SK_ENTITY:
            return self.SK_ENTITY

        return self.PK_ENTITY

    @property
    def pk(self) -> str:
        if not self.PK_ENTITY or not self.PK_FIELD:
            raise Exception("Model must have a PK_ENTIY & PK_FIELD set")

        return f"{self.PK_ENTITY}#{getattr(self.model, self.PK_FIELD)}"

    @property
    def sk(self) -> str:
        return (
            f"{self.SK_ENTITY}#{getattr(self.model, self.SK_FIELD)}"
            if self.SK_ENTITY
            else self.pk
        )

    @property
    def key(self) -> dict:
        return {
            "pk": self.pk,
            "sk": self.sk,
        }

    @property
    def item(self) -> dict:
        item: dict = json.loads(self.model.json())

        if not item:
            raise Exception

        item["pk"] = self.pk
        item["sk"] = self.sk
        item["entity"] = self.entity

        return item

    @classmethod
    def get_models_key(
        cls,
        model: BaseModel,
    ) -> dict:
        pk: str = f"{cls.PK_ENTITY}#{getattr(model, cls.PK_FIELD)}"
        sk: str = (
            f"{cls.SK_ENTITY}#{getattr(model, cls.SK_FIELD)}" if cls.SK_ENTITY else pk
        )
        return {
            "pk": f"{cls.PK_ENTITY}#{getattr(model, cls.PK_FIELD)}",
            "sk": sk,
        }

    @classmethod
    def get_domain_model(cls, domain_data: dict) -> BaseModel:
        return cls.DOMAIN_MODEL(**domain_data)
