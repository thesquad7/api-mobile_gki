from datetime import date, datetime, time
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Acara
import config.upload
from SchemasIndex import AcaraUpdate,AcaraCreate
from .login import user_refs
import os
from config.setting import db_dependency

route_acara= APIRouter(prefix="/admin", tags=['Acara'])
api_id : str
api_address_long= "/acara/{api_id}"
api_address = "/acara/"
Upload_Directory = config.upload.ACARA_IMG_DIR
api_baseModelCreate = AcaraCreate
api_baseModelUpdate = AcaraUpdate
api_ModelsDB = Acara
detail_identity = "acara"


#========================================================CRUD ROOM======================================================
@route_acara.post(api_address)
async def acara_add(user:user_refs,db:db_dependency, name: str = Form(...),content: str = Form(...),status:str= Form(...),tanggal: date=Form(...),category_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and file and content and  tanggal and category_id and status):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = api_ModelsDB(name= name,content= content, tanggal=tanggal, category_id=category_id,status=status, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_acara.put(api_address_long)
async def acara_update(user:user_refs,api_id:int,db:db_dependency, name: str = Form(...),status:str= Form(...),content: str = Form(...),tanggal: date=Form(...),category_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and file and content and tanggal and status and category_id):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    if db_show.content_img != f'{Upload_Directory}{file.filename}':
        delete_temp = f'{db_show.content_img}'
        if os.path.exists(delete_temp):
            os.remove(delete_temp)
            status = "Photo Berubah"
        status_os = status
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_update= api_baseModelUpdate(name=name, content= content, tanggal=tanggal,status=status, category_id=category_id,content_img=path,updated_at=datetime.now)
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status_os
    return {"message": response }
1
@route_acara.delete(api_address_long)
async def delete_acara(user:user_refs,api_id: int, db:db_dependency):
    db_delete=db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_delete is None:
        raise HTTPException(status_code=404, detail="Informasi "+detail_identity+" tidak ditemukan")
    delete_temp = f'{db_delete.content_img}'
    if os.path.exists(delete_temp):
        os.remove(delete_temp)
        status = "Gambar di Hapus"
    os_delete_status = status
    db.delete(db_delete)
    db.commit()
    response = "Informasi "+detail_identity+ " telah di hapus," + os_delete_status
    return {"message": response}

@route_acara.get(api_address_long)
async def acara_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_acara.get(api_address)
async def acara_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    return db_show