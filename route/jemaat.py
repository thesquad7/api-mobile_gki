from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Jemaats
import config.upload
from datetime import date, datetime
from SchemasIndex import JemaatUpdate,JemaatCreate
from .login import user_refs
import os
from config.setting import db_dependency

route_jemaat= APIRouter(prefix="/admin", tags=['Jemaat'])
api_id : str
api_address_long= "/jemaat/{api_id}"
api_address = "/jemaat/"
Upload_Directory = config.upload.JEMAAT_IMG_DIR
api_baseModelCreate = JemaatCreate
api_baseModelUpdate = JemaatUpdate
api_ModelsDB = Jemaats
detail_identity = "jemaat"


#========================================================CRUD ROOM======================================================
@route_jemaat.post(api_address)
async def jemaat_add(user:user_refs,db:db_dependency,pendeta_id: str =Form(...),jemaat_id: str =Form(...),name: str =Form(...),tempat_lahir: str =Form(...),tanggal_lahir: date =Form(...),n_bapak: str =Form(...),n_ibu: str =Form(...),n_baptis: str =Form(...), alamat: str = Form(...), file: UploadFile = File(...)):
    if not (name and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = api_ModelsDB(name= name,jemaat_id=jemaat_id,pendeta_id=pendeta_id,tempat_lahir=tempat_lahir,tanggal_lahir=tanggal_lahir,nama_bapak=n_bapak,nama_ibu=n_ibu,nama_baptis=n_baptis,alamat=alamat, jemaat_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_jemaat.put(api_address_long)
async def jemaat_update(user:user_refs,db:db_dependency,api_id:int,pendeta_id: str =Form(...),jemaat_id: str =Form(...),name: str =Form(...),tempat_lahir: str =Form(...),tanggal_lahir: date =Form(...),n_bapak: str =Form(...),n_ibu: str =Form(...),n_baptis: str =Form(...), alamat: str = Form(...), file: UploadFile = File(...)):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if not (name and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    if db_show.jemaat_img != f'{Upload_Directory}{file.filename}':
        delete_temp = f'{db_show.jemaat_img}'
        if os.path.exists(delete_temp):
            os.remove(delete_temp)
            status = "Photo Berubah"
        status = ""
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_update= api_baseModelUpdate(name= name,jemaat_id=jemaat_id,pendeta_id=pendeta_id,tempat_lahir=tempat_lahir,tanggal_lahir=tanggal_lahir,nama_bapak=n_bapak,nama_ibu=n_ibu,nama_baptis=n_baptis,alamat=alamat, jemaat_img=path,updated_at=datetime.now)
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status
    return {"message": response }
1
@route_jemaat.delete(api_address_long)
async def delete_jemaat(user:user_refs,api_id: int, db:db_dependency):
    db_delete=db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_delete is None:
        raise HTTPException(status_code=404, detail="Informasi "+detail_identity+" tidak ditemukan")
    delete_temp = f'{db_delete.jemaat_img}'
    if os.path.exists(delete_temp):
        os.remove(delete_temp)
        status = "Gambar di Hapus"
    os_delete_status = status
    db.delete(db_delete)
    db.commit()
    response = "Informasi "+detail_identity+ " telah di hapus," + os_delete_status
    return {"message": response}

@route_jemaat.get(api_address_long)
async def jemaat_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_jemaat.get(api_address)
async def jemaat_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    modified_data = [{"alamat": item.alamat, "jemaat_id": item.jemaat_id, "name": item.name, "j_pic": item.jemaat_img} for item in db_show]
    return modified_data
