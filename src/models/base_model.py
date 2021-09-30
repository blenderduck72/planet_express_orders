# import simplejson as json

# from pydantic import BaseModel as PydanticModel

# # EXCLUDED_FIELDS: dict = {
# #     "key": ...,
# # }


# class BaseModel(PydanticModel):

#     PK_ENTITY: str = None
#     SK_ENTITY: str = None
#     PK_FIELD: str = None
#     SK_FIELD: str = None

#     @property
#     def entity(self) -> str:
#         if self.SK_ENTITY:
#             return self.SK_ENTITY

#         return self.PK_ENTITY

#     @property
#     def pk(self) -> str:
#         if not self.PK_ENTITY or not self.PK_FIELD:
#             raise Exception("Model must have a PK_ENTIY & PK_FIELD set")
#         return f"{self.PK_ENTITY}#{getattr(self, self.PK_FIELD)}"

#     @property
#     def sk(self) -> str:
#         if not self.SK_ENTITY:
#             return self.pk
#         else:
#             sk: str = f"{self.SK_ENTITY}#{getattr(self, self.SK_FIELD)}"

#     @property
#     def key(self) -> dict:
#         return {
#             "pk": self.pk,
#             "sk": self.sk,
#         }

#     @classmethod
#     def _get_properties(cls):
#         return [
#             prop
#             for prop in dir(cls)
#             if isinstance(getattr(cls, prop), property)
#             and prop not in ("__values__", "fields")
#         ]

#     # def dict(
#     #     self,
#     #     *,
#     #     include: dict = None,
#     #     exclude: dict = None,
#     #     by_alias: bool = False,
#     #     skip_defaults: bool = None,
#     #     exclude_unset: bool = False,
#     #     exclude_defaults: bool = True,
#     #     exclude_none: bool = False,
#     # ) -> dict:

#     #     if exclude:
#     #         excluded_fields: dict = exclude.union(EXCLUDED_FIELDS)
#     #     else:
#     #         excluded_fields: dict = EXCLUDED_FIELDS
#     #         import pdb

#     #         pdb.set_trace()
#     #     data: dict = super().dict(
#     #         include=include,
#     #         exclude=excluded_fields,
#     #         by_alias=by_alias,
#     #         skip_defaults=skip_defaults,
#     #         exclude_unset=exclude_unset,
#     #         exclude_defaults=exclude_defaults,
#     #         exclude_none=exclude_none,
#     #     )
#     #     props = self._get_properties()
#     #     if include:
#     #         props = [prop for prop in props if prop in include]
#     #     if excluded_fields:
#     #         props = [prop for prop in props if prop not in excluded_fields]

#     #     if props:
#     #         data.update({prop: getattr(self, prop) for prop in props})

#     #     return data

#     # def to_json(self) -> str:
#     #     return self.json(exclude_defaults=True)

#     # def to_item(self) -> dict:
#     #     return json.loads(self.to_json())
