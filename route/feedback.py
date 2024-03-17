from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Feedback
import config.upload
from SchemasIndex import FeedbackUpdate,FeedbackRequest
from .login import user_refs
import os
from config.setting import db_dependency

route_feedback= APIRouter(prefix="/admin", tags=['Masukan'])
api_id : str
api_address_long= "/address/{api_id}"
api_address = "/address/"
Upload_Directory = config.upload.FEEDBACK_IMG_DIR
api_baseModelCreate = FeedbackRequest
api_baseModelUpdate = FeedbackUpdate
api_ModelsDB = Feedback
detail_identity = "masukan"


#========================================================CRUD ROOM======================================================
@route_feedback.post(api_address)
async def gereja_add(db:db_dependency, name: str = Form(...),content:str= Form(...),file: UploadFile = File(...)):
    if not (name and content and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = api_ModelsDB(name= name,content=content, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan, Terimakasih!!"}

@route_feedback.delete(api_address_long)
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

@route_feedback.get(api_address_long)
async def gereja_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_feedback.get(api_address)
async def gereja_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    return db_show