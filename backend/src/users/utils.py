import datetime
from datetime import timedelta, timezone
import jwt
from pwdlib import PasswordHash
from src.config import settings

pwhash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwhash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwhash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(timezone.utc) + expires_delta
    else:
        
        expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=30) 
    
    to_encode.update({"exp": expire})
    
    
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt