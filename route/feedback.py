from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Feedback
import config.upload
from SchemasIndex import FeedbackUpdate,FeedbackRequest
from .login import user_refs
import os
from PIL import Image
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
async def feedback_add(db:db_dependency, name: str = Form(...),content:str= Form(...),file: UploadFile = File(...)):
    if not (name and content and file):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = os.path.join(Upload_Directory, file.filename)
         temp_path = os.path.join(Upload_Directory, f"temp_{file.filename}")
         with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
         with Image.open(temp_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(path, "JPEG", optimize=True, quality=70)
         os.remove(temp_path)
         db_input = api_ModelsDB(name= name,content=content, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan, Terimakasih!!"}

@route_feedback.delete(api_address_long)
async def delete_feedback(user:user_refs,api_id: int, db:db_dependency):
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
async def feedback_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    return db_show

@route_feedback.get(api_address)
async def feedback_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    return db_show