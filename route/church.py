from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Church
import config.upload
from SchemasIndex import ChurchUpdate
from .login import user_refs
import os
from config.setting import db_dependency

route_gereja= APIRouter(prefix="/admin", tags=['Gereja'])

#========================================================Pendeta CRUD ROOM======================================================
@route_gereja.post("/gereja/")
async def gereja_add(user:user_refs,db:db_dependency, name: str = Form(...), file: UploadFile = File(...)):
    if not (name and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{config.upload.GEREJA_IMG_DIR}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = Church(name= name, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": "Gereja telah di tambahkan"}

@route_gereja.put("/gereja/{gereja_id}")
async def gereja_update(user:user_refs,db:db_dependency,gereja_id:int, name: str = Form(...), file: UploadFile = File(...)):
    db_show = db.query(Church).filter(Church.id == gereja_id).first()
    if not (name and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    if db_show.content_img != f'{config.upload.GEREJA_IMG_DIR}{file.filename}':
        delete_temp = f'{db_show.content_img}'
        if os.path.exists(delete_temp):
            os.remove(delete_temp)
            status = "Photo Berubah"
        status = ""
    try:
         path = f'{config.upload.GEREJA_IMG_DIR}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_update= ChurchUpdate(name=name,content_img=path)
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    return {"message": "Identitas Identitas telah berubah,{status}" }

@route_gereja.delete("/gereja/{gereja_id}")
async def delete_pendeta(user:user_refs,gereja_id: int, db:db_dependency):
    db_delete=db.query(Church).filter(Church.id == gereja_id).first()
    if db_delete is None:
        raise HTTPException(status_code=404, detail="Informasi gereja tidak ditemukan")
    db.delete(db_delete)
    db.commit()
    return {"message": "Informasi Gereja telah di hapus"}

@route_gereja.get("/gereja/{gereja_id}")
async def gereja_one(user:user_refs,gereja_id:int, db:db_dependency):
    db_show = db.query(Church).filter(Church.id == gereja_id).first()
    return db_show

@route_gereja.get("/gereja/")
async def gereja_all(user:user_refs, db:db_dependency):
    db_show = db.query(Church).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi gereja belum tersedia")
    return db_show