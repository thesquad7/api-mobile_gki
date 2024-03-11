from passlib.context import CryptContext
from fastapi import HTTPException, status,Depends
from models.index import User
from sqlalchemy.orm import Session
from typing import Annotated
from jose import JWTError, jwt
from config.db import engine, LocalSession, Base

def get_db():
    db= LocalSession()
    try:
        yield db
    finally:
        db.close()
db = Annotated[Session, Depends(get_db)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to generate JWT token
def create_access_token(data: dict):
    return jwt.encode(data, "SECRET_KEY", algorithm="HS256")

# Function to authenticate user
def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return user
