import simplejson as json
from pydantic import BaseModel


class DynamoItem(BaseModel):
    _PK_ENTITY: str
    _PK_FIELD: str
    _SK_ENTITY: str
    _SK_FIELD: str

    """
    Represents a DynamoItem

    ...

    Attributes
    ----------
    _PK_ENTITY : str
        Entity name of the Partition Key.
    _PK_FIELD : str
        Field with a value used to form a Partition Key.
    _SK_ENTITY : str
        Entity name of the Sort Key.
    _SK_FIELD: str
        Field with a value used to form the Sort Key.


    Methods
    -------
    entity() -> str
        Returns the model's calculated entity.

    key() -> str
        Returns the calculated key of the model.

    pk() -> str
        Returns the calculated Partition Key.

    sk() -> str
        Returns the calcualted Sort Key.

    Class Methods
    -------
    calculate_key(pk_value: str, sk_value: str) -> dict
        Accepts two values and returns a calculated DynamoDB key.
    """

    @property
    def entity(self) -> str:
        """
        Returns:
            entity (str): The computed entity of the model.
        """
        if self._SK_ENTITY:
            return self._SK_ENTITY

        return self._PK_ENTITY

    @property
    def key(self) -> dict:
        """
        Returns:
            key (dict) : Calcuated DynamoDB Key Dictionary.
        """
        return {
            "pk": self.pk,
            "sk": self.sk,
        }

    @property
    def pk(self) -> str:
        """
        Returns:
            pk (str): The computed Partition Key value.

        Raises:
            exception (Exception) : Raises standard Exception.

        """
        if not self._PK_ENTITY or not self._PK_FIELD:
            raise Exception("Model must have a PK_ENTIY & PK_FIELD set")

        return f"{self._PK_ENTITY}#{getattr(self, self._PK_FIELD)}"

    @property
    def sk(self) -> str:
        """
        Returns:
            sk (str): The computed Sort Key value.
        """
        return (
            f"{self._SK_ENTITY}#{getattr(self, self._SK_FIELD)}"
            if self._SK_ENTITY
            else self.pk
        )

    @property
    def item(self) -> dict:
        """
        Returns:
            item (dict) : Saveable DynamoDB Dictionary
        """
        item: dict = json.loads(self.json())
        if not item:
            raise Exception

        item["pk"] = self.pk
        item["sk"] = self.sk
        item["entity"] = self.entity

        return item

    @classmethod
    def calculate_key(
        cls,
        pk_value: str or int,
        sk_value: str or int or None = None,
    ) -> dict:
        """
        Calculates what should be a DynamoDB key based off
        the provided pk_value, and sk_value

        Arguments:
            pk_value (str): Value used for the pk_field
            sk_value (str): Value used for the sk_field

        Returns:
            key (dict) : Calcuated DynamoDB Key Dictionary.
        """
        pk: str = f"{cls._PK_ENTITY}#{str(pk_value)}"

        if cls._SK_ENTITY is None:
            return {"pk": pk, "sk": pk}

        if sk_value is None:
            raise Exception("SK value is required to calculate key on this Item.")
        return {"pk": pk, "sk": f"{cls._SK_ENTITY}#{str(sk_value)}"}
