from typing import Annotated
from config.db import LocalSession
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends

SECRET_KEY = "148bebf7123c3b4a2fa9acde2bae7f367d590b5708d9bac268953cde72a86f6a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MUNITES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
def get_db():
    db= LocalSession()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
