from pydantic import Field

from .base_schemas import BaseModel


class CourseScheme(BaseModel):
    id: int
    name: str
    description: str


class CourseCreateScheme(BaseModel):
    name: str
    description: str = Field(default=None)


class CourseUpdateScheme(BaseModel):
    name: str = Field(default=None)
    description: str = Field(default=None)


