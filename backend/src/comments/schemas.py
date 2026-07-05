from pydantic import BaseModel, Field
from datetime import datetime
from src.users.schemas import UserShortSchema

class CommentBaseSchema(BaseModel):
    content: str = Field(min_length=1, max_length=1000)

class CommentCreateSchema(CommentBaseSchema):
    pass

class CommentResponseSchema(CommentBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserShortSchema

    class Config:
        from_attributes = True

class CommentUpdateSchema(BaseModel):
    content: str | None = Field(None, min_length=1, max_length=1000)