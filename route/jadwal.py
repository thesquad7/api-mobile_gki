from datetime import date, datetime, time
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Jadwal
import config.upload
from SchemasIndex import JadwalCreate,JadwalUpdate
from .login import user_refs
import os
from config.setting import db_dependency

route_jadwal= APIRouter(prefix="/admin", tags=['Jadwal'])
api_id : str
api_address_long= "/jadwal/{api_id}"
api_address = "/jadwal/"
Upload_Directory = config.upload.JADWAL_IMG_DIR
api_baseModelCreate = JadwalCreate
api_baseModelUpdate = JadwalUpdate
api_ModelsDB = Jadwal
detail_identity = "jadwal"


#========================================================CRUD ROOM======================================================
@route_jadwal.post(api_address)
async def jadwal_add(user:user_refs,db:db_dependency, title: str = Form(...),content: str = Form(...),waktu_mulai: time = Form(...),tanggal_mulai: date=Form(...),pendeta_id:int=Form(...), file: UploadFile = File(...)):
    if not (title and file and content and waktu_mulai and tanggal_mulai and pendeta_id):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = api_ModelsDB(title= title,content= content, waktu_mulai=waktu_mulai, tanggal_mulai=tanggal_mulai, pendeta_id=pendeta_id, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_jadwal.put(api_address_long)
async def jadwal_update(user:user_refs,api_id:int,db:db_dependency, title: str = Form(...),content: str = Form(...),waktu_mulai: time = Form(...),tanggal_mulai: date=Form(...),pendeta_id:int=Form(...), file: UploadFile = File(...)):
    if not (title and file and content and waktu_mulai and tanggal_mulai and pendeta_id):
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
         db_update= api_baseModelUpdate(title=title, content= content,waktu_mulai=waktu_mulai, tanggal_mulai=tanggal_mulai, pendeta_id=pendeta_id,content_img=path,updated_at=datetime.now)
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status
    return {"message": response }
1
@route_jadwal.delete(api_address_long)
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

@route_jadwal.get(api_address_long)
async def jadwal_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_jadwal.get(api_address)
async def jadwal_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    return db_show