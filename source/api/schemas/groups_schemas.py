from pydantic import Field

from .base_schemas import BaseModel


class GroupScheme(BaseModel):
    id: int
    name: str


class GroupCreateScheme(BaseModel):
    name: str


class GroupUpdateScheme(BaseModel):
    name: str = Field(default=None)
