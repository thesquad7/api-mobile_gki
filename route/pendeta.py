from datetime import datetime
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Pendeta
import config.upload
from SchemasIndex import PendetaUpdate
from .login import user_refs
from config.setting import db_dependency

route_pendeta= APIRouter(prefix="/admin", tags=['Pendeta'])

#========================================================Pendeta CRUD ROOM======================================================
@route_pendeta.post("/pendeta/")
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

@route_pendeta.put("/pendeta/{pendeta_id}")
async def pendeta_update(user:user_refs,db:db_dependency,pendeta_id:int, name: str = Form(...),status: str = Form(...), file: UploadFile = File(...)):
    db_show = db.query(Pendeta).filter(Pendeta.id == pendeta_id).first()
    if not (name and status and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{config.upload.PENDETA_IMG_DIR}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_update= PendetaUpdate(name=name, status=status,profile_img=path, updated_at=datetime.now(),)
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    return {"message": "Identitas Pendeta telah berubah"}

@route_pendeta.put("/pendeta_no_img/{pendeta_id}")
async def pendeta_update_noimage(user:user_refs,db:db_dependency,pendeta_id:int, name: str = Form(...),status: str = Form(...)):
    db_show = db.query(Pendeta).filter(Pendeta.id == pendeta_id).first()
    try:
        
         db_update= PendetaUpdate(name=name, status=status, updated_at=datetime.now(),)
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    return {"message": "Identitas Pendeta telah berubah"}
@route_pendeta.delete("/pendeta/{pendeta_id}")
async def delete_pendeta(user:user_refs,pendeta_id: int, db:db_dependency):
    db_delete=db.query(Pendeta).filter(Pendeta.id == pendeta_id).first()
    if db_delete is None:
        raise HTTPException(status_code=404, detail="Informasi pendeta tidak ditemukan")
    db.delete(db_delete)
    db.commit()
    return {"message": "Informasi Pendeta telah di hapus"}

@route_pendeta.get("/pendeta/{pendeta_id}")
async def pendeta_one(user:user_refs,pendeta_id:int, db:db_dependency):
    db_show = db.query(Pendeta).filter(Pendeta.id == pendeta_id).first()
    return db_show

@route_pendeta.get("/pendeta/")
async def pendeta(user:user_refs, db:db_dependency):
    db_show = db.query(Pendeta).all()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi pendeta belum tersedia")
    return db_show