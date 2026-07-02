from pydantic import BaseModel, EmailStr, Field

class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    username: str | None = None