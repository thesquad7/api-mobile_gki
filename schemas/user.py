from pydantic import BaseModel

class User(BaseModel):
    username : str
    name : str
    password : str


class UserResponse(BaseModel):
    id : int
    username : str
    name : str
    user_pic : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str
    credential: int

class TokenData(BaseModel):
    username : str or None = None


class UserInDB(User):
    password : str

class UserRequest(BaseModel):
    username: str
    password: str
    name : str