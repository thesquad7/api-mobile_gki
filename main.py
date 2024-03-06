from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext

SECRET_KEY = "148bebf7123c3b4a2fa9acde2bae7f367d590b5708d9bac268953cde72a86f6a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MUNITES = 30

db= {
    "tim":{
        "username": "tim",
        "fullname": "timtam",
        "email": "email@emai.com",
        "hashed_password": "$2b$12$9nDbBWmnZEKLG3Yo2ko2I.Is44cmlpBgxu71JHqbjGmGxeJMq0DhC",
        "disable":False
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username : str or None = None

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username:str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)

def auth_user(db, username:str, password:str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    
    return user

def create_access_token(data:dict, expires_deta: timedelta or None = None):
    to_encode = data.copy()
    if expires_deta:
        expire = datetime.utcnow() + expires_deta
    else:
        expire =  datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_curent_user(token: str = Depends(oauth_2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="How Are You?", headers={"WWW-Authenticate : Bearer"})
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data= TokenData(username=username)

    except JWTError:
        raise credential_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user
async def get_current_active_user(current_user: UserInDB = Depends(get_curent_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="User AFK")
    
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm= Depends()):
    user = auth_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User dan Password Salah", headers={"WWW-Authenticate : Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MUNITES)
    access_token = create_access_token(data={"sub": user.username}, expires_deta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/me/", response_model=User)
async def read_user_me(curent_user: User = Depends(get_current_active_user)):
    return curent_user

@app.get("/user/me/items")
async def read_own_items(curent_user: User = Depends(get_current_active_user)):
    return [{"item_id":1 , "owner": curent_user}]