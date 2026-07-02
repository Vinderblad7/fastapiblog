from fastapi import APIRouter, HTTPException, status 
from sqlalchemy import select, or_
from src.dependencies import SessionDep
from src.users.schemas import UserRegisterSchema, UserResponseSchema
from src.users.models import UserModel
from src.users.utils import hash_password 

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.users.schemas import TokenSchema
from src.users.utils import verify_password, create_access_token
from typing import Annotated


users_router = APIRouter(prefix="/auth", tags=["Auth"])

@users_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegisterSchema, session: SessionDep):

    query = await session.execute(
        select(UserModel).where(
            or_(
                UserModel.email == data.email,
                UserModel.username == data.username
            )
        )
    )
    
    user = query.scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
        
    hashed_pwd = hash_password(data.password)
    
    new_user = UserModel(
        email=data.email,
        username=data.username,
        hashed_password=hashed_pwd
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@users_router.post("/login", response_model=TokenSchema)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    query = await session.execute(
        select(UserModel).where(
            or_(
                UserModel.email == form_data.username,
                UserModel.username == form_data.username
            )
        )
    )
    user = query.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}