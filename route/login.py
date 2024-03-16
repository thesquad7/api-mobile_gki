from fastapi import Depends, HTTPException, UploadFile, status, APIRouter,Form,File
from jose import JWTError,jwt
from typing import Annotated
from ModelIndex import Pendeta, Category
from schemas.index import CategoryCreate
import config.upload
from config.setting import SECRET_KEY, ALGORITHM, db_dependency, oauth2_bearer

route_login = APIRouter(prefix="/api/v1", tags=['Login'])

async def get_user_active(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User tidak ter validasi')
        return{'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User tidak dapat diketahui')

user_refs = Annotated[dict, Depends(get_user_active)]

def save_file_and_data(db, item_name: str, item_status: str, file: UploadFile):
    file_name = file.filename
    with open(file_name, "wb") as file_object:
        file_object.write(file.file.read())

    db_item = Pendeta(name=item_name, status=item_status, file_name=file_name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@route_login.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_refs, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Auth Gagal')
    return {"User": user}


