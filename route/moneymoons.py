from datetime import datetime
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Money
import config.upload
from SchemasIndex import MoneyMoonUpdate,MoneyMoonRequest,MoneyMoonCreate,MoneyMoonUpdatePUT
from .login import user_refs
from config.setting import db_dependency

route_money= APIRouter(prefix="/admin", tags=['Persembahan'])
api_id : str
api_address_long= "/persembahan/{api_id}"
api_address = "/persembahan/"
Upload_Directory = config.upload.GEREJA_IMG_DIR
api_baseModelCreate = MoneyMoonCreate
api_baseModelUpdate = MoneyMoonRequest
api_ModelsDB = Money
detail_identity = "laporan persembahan"


#========================================================CRUD ROOM======================================================
@route_money.post(api_address)
async def persembahan_add(user:user_refs,db:db_dependency, body:api_baseModelUpdate):
    if not (body):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    try:
         db_input = api_ModelsDB(**body.dict())
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_money.put(api_address_long)
async def persembahan_update(user:user_refs,db:db_dependency,body:api_baseModelUpdate):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if not (body):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    try:
    
         db_update= MoneyMoonUpdatePUT(**body.dict(),updated_at=datetime.now)
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, "
    return {"message": response }

@route_money.delete(api_address_long)
async def delete_persembahan(user:user_refs,api_id: int, db:db_dependency):
    db_delete=db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_delete is None:
        raise HTTPException(status_code=404, detail="Informasi "+detail_identity+" tidak ditemukan")
    db.delete(db_delete)
    db.commit()
    response = "Informasi "+detail_identity+ " telah di hapus,"
    return {"message": response}

@route_money.get(api_address_long)
async def persembahan_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_money.get(api_address)
async def persembahan_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    return db_show