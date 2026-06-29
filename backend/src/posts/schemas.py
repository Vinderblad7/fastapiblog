from pydantic import BaseModel, Field
from datetime import datetime

class TagBaseSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100)


class TagCreateSchema(TagBaseSchema):
    pass

class TagResponseSchema(TagBaseSchema):
    id: int

    class Config:
        from_attributes = True

class PostBaseSchema(BaseModel):
    title: str = Field(min_length=3, max_length=155)
    content: str = Field(min_length=3, max_length=1000)

class PostCreateSchema(PostBaseSchema):
    tags_ids: list[int] = Field(default=[])

class PostResponseSchema(PostBaseSchema):

    id: int
    tags: list[TagResponseSchema]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostUpdateSchema(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=155)
    content: str | None = Field(None, min_length=3, max_length=1000)