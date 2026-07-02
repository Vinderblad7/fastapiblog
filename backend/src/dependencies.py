from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_session
from src.users.models import UserModel
from src.users.schemas import TokenDataSchema

SessionDep = Annotated[AsyncSession, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login") 

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
) -> UserModel:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenDataSchema(username=username)
        
    except InvalidTokenError:
        raise credentials_exception
        
    query = await session.execute(select(UserModel).where(UserModel.username == token_data.username))
    user = query.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    return user

CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]