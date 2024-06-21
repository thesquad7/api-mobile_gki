from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Kesaksian
import config.upload
from SchemasIndex import KesaksianUpdate,KesaksianCreate
from .login import user_refs
import os
from datetime import date, datetime
from config.setting import db_dependency

route_kesakian= APIRouter(prefix="/admin", tags=['Kesaksian'])
api_id : str
api_address_long= "/kesaksian/{api_id}"
api_address = "/kesaksian/"
Upload_Directory = config.upload.KESAKSIAN_IMG_DIR
api_baseModelCreate = KesaksianCreate
api_baseModelUpdate = KesaksianUpdate
api_ModelsDB = Kesaksian
detail_identity = "kesaksian"


#========================================================CRUD ROOM======================================================
@route_kesakian.post(api_address)
async def jadwal_add(user:user_refs,db:db_dependency, name: str = Form(...),date:date=Form(...),status: str = Form(...),user_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and status and file and user_id and date):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = api_ModelsDB(name= name,status= status,user_id=user_id,date=date, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_kesakian.put(api_address_long)
async def jadwal_update(user:user_refs,api_id:int,db:db_dependency, name: str = Form(...),date:date = Form(...),status: str = Form(...),user_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and file and status and user_id and date):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    if db_show.content_img != f'{Upload_Directory}{file.filename}':
        delete_temp = f'{db_show.content_img}'
        if os.path.exists(delete_temp):
            os.remove(delete_temp)
            status = "Photo Berubah"
        status = ""
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_update= api_baseModelUpdate(name=name, status= status,user_id=user_id, date=date,content_img=path,updated_at=datetime.now)
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status
    return {"message": response }

@route_kesakian.delete(api_address_long)
async def delete_jadwal(user:user_refs,api_id: int, db:db_dependency):
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

@route_kesakian.get(api_address_long)
async def jadwal_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_kesakian.get(api_address)
async def jadwal_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    return db_show