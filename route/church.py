from datetime import datetime
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Church
import config.upload
from SchemasIndex import ChurchUpdate,CategoryCreate,ChurchUpdateNoImage
from .login import user_refs
import os
from config.setting import db_dependency

route_gereja= APIRouter(prefix="/admin", tags=['Gereja'])
api_id : str
api_address_long= ["/gereja/{api_id}","/gereja_no_image/{api_id}"]
api_address = "/gereja/"
Upload_Directory = config.upload.GEREJA_IMG_DIR
api_baseModelCreate = CategoryCreate
api_baseModelUpdate = [ChurchUpdate,ChurchUpdateNoImage]
api_ModelsDB = Church
detail_identity = "gereja"


#========================================================CRUD ROOM======================================================
@route_gereja.post(api_address)
async def gereja_add(user:user_refs,db:db_dependency, name: str = Form(...), file: UploadFile = File(...)):
    if not (name and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = api_ModelsDB(name= name, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_gereja.put(api_address_long[0])
async def gereja_update(user:user_refs,db:db_dependency,api_id:int, name: str = Form(...), file: UploadFile = File(...)):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if not (name and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
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
         db_update= api_baseModelUpdate[0](name=name,content_img=path,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status
    return {"message": response }

@route_gereja.put(api_address_long[1])
async def gereja_update(user:user_refs,db:db_dependency,api_id:int, name: str = Form(...), ):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if not name:
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    try:
         db_update= api_baseModelUpdate[1](name=name,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah"
    return {"message": response }

@route_gereja.delete(api_address_long[0])
async def delete_pendeta(user:user_refs,api_id: int, db:db_dependency):
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

@route_gereja.get(api_address_long[0])
async def gereja_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_gereja.get(api_address)
async def gereja_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    return db_show