from fastapi import Depends, HTTPException, UploadFile, status, APIRouter,Form,File
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from sqlalchemy.orm import Session
from typing import Annotated
from models.index import Pendeta
from config.db import LocalSession
import config.upload
from config.setting import SECRET_KEY, ALGORITHM

route_login = APIRouter(prefix="/api/v1", tags=['Login'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
def get_db():
    db= LocalSession()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

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


@route_login.post("/pendeta/")
async def pendeta(user:user_refs,db:db_dependency, name: str = Form(...),status: str = Form(...), file: UploadFile = File(...)):
    if not (name and status and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{config.upload.PENDETA_IMG_DIR}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = Pendeta(name= name, status= status, profile_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": "Pendeta telah di tambahkan"}

# @route_login.post("/pendeta/", status_code=status.HTTP_201_CREATED)
# async def create_pendeta(user: user_refs,pendeta: PendetaRequest,file:UploadFile, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Memerlukan Akses')
#     path = f'{config.upload.PENDETA_IMG_DIR}{file.filename}'
#     with open(path, "wb") as buffer:
#         buffer.write(await file.read())
#     db_pendeta=Pendeta(name = pendeta.name, status=pendeta.status, profile_img=path)
#     db.add(db_pendeta)
#     db.commit()