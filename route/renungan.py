from datetime import date, datetime, time
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Renungan
import config.upload
from SchemasIndex import RenunganCreate,RenunganUpdate
from .login import user_refs
import os
from PIL import Image
from config.setting import db_dependency

route_renungan= APIRouter(prefix="/admin", tags=['Renungan'])
api_id : str
api_address_long= "/renungan/{api_id}"
api_address = "/renungan/"
Upload_Directory = config.upload.RENUNGAN_IMG_DIR
api_baseModelCreate = RenunganCreate
api_baseModelUpdate = RenunganUpdate
api_ModelsDB = Renungan
detail_identity = "renungan"


#========================================================CRUD ROOM======================================================
@route_renungan.post(api_address)
async def renungan_add(user:user_refs,db:db_dependency, name: str = Form(...),content: str = Form(...),tanggal: date=Form(...),category_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and file and content and  tanggal and category_id ):
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
         db_input = api_ModelsDB(name= name,content= content, tanggal=tanggal, category_id=category_id, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_renungan.put(api_address_long)
async def renungan_update(user:user_refs,api_id:int,db:db_dependency, name: str = Form(...),content: str = Form(...),tanggal: date=Form(...),category_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and file and content and tanggal and category_id):
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
         db_update= api_baseModelUpdate(name=name, content= content, tanggal=tanggal, category_id=category_id,content_img=path,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status_os
    return {"message": response }

@route_renungan.delete(api_address_long)
async def delete_renungan(user:user_refs,api_id: int, db:db_dependency):
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

@route_renungan.get(api_address_long)
async def renungan_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    category = db_show.category
    jadwal_dict ={
        "id" : db_show.id,
            "name" : db_show.name,
            "tanggal" : db_show.tanggal,
            "content_img":db_show.content_img,
            "content": db_show.content,
            "category":{
                "id" :  category.id if category else None,
            },
    }
    return jadwal_dict

@route_renungan.get(api_address)
async def renungan_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    result = []
    for jadwal in db_show:
        category = jadwal.category
        color_id = category.color_id if category else None
        jadwal_dict ={
            "id" : jadwal.id,
            "name" : jadwal.name,
            "tanggal" : jadwal.tanggal,
            "content_img":jadwal.content_img,
            "content": jadwal.content,
            "category":{
                "name" :  category.name if category else None,
                "color_id": color_id
            },
              
        }
        result.append(jadwal_dict)
    return result