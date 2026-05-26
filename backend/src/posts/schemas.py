from pydantic import BaseModel, Field
from datetime import datetime


class PostBaseSchema(BaseModel):
    title: str = Field(min_length=3, max_length=155)
    content: str = Field(min_length=3, max_length=1000)

class PostCreateSchema(PostBaseSchema):
    pass

class PostResponseSchema(PostBaseSchema):

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
