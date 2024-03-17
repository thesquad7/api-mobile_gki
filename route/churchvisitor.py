from datetime import date, time
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import ChurchVisitor
import config.upload
from SchemasIndex import ChurchVUpdate,ChurchVRequest
from .login import user_refs
import os
from config.setting import db_dependency

route_visitor= APIRouter(prefix="/admin", tags=['Visitor'])
api_id : str
api_address_long= "/visitor/{api_id}"
api_address = "/visitor/"
api_baseModelCreate = ChurchVRequest
api_baseModelUpdate = ChurchVUpdate
api_ModelsDB = ChurchVisitor
detail_identity = "pengunjung gereja"


#========================================================CRUD ROOM======================================================
@route_visitor.post(api_address)
async def visitor_add(user:user_refs,db:db_dependency, body:api_baseModelUpdate):
    if not (body):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    try:
         db_input = api_ModelsDB(**body.dict())
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_visitor.put(api_address_long)
async def visitor_update(user:user_refs,api_id:int,db:db_dependency, body:ChurchVUpdate):
    if not (body):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    try:
         db_update= api_baseModelUpdate(**body.dict())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, "
    return {"message": response }
1
@route_visitor.delete(api_address_long)
async def delete_visitor(user:user_refs,api_id: int, db:db_dependency):
    db_delete=db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_delete is None:
        raise HTTPException(status_code=404, detail="Informasi "+detail_identity+" tidak ditemukan")
    db.delete(db_delete)
    db.commit()
    response = "Informasi "+detail_identity+ " telah di hapus,"
    return {"message": response}

@route_visitor.get(api_address_long)
async def visitor_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_visitor.get(api_address)
async def visitor_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if not (db_show) :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    return db_show