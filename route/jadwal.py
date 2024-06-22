from datetime import date, datetime, time
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Jadwal
import config.upload
from PIL import Image
from SchemasIndex import JadwalCreate,JadwalUpdate,JadwalUpdateNoImage
from .login import user_refs
import os
from config.setting import db_dependency

route_jadwal= APIRouter(prefix="/admin", tags=['Jadwal'])
api_id : str
api_address_long= ["/jadwal/{api_id}","/jadwal_no_image/{api_id}"]
api_address = "/jadwal/"
Upload_Directory = config.upload.JADWAL_IMG_DIR
api_baseModelCreate = JadwalCreate
api_baseModelUpdate = [JadwalUpdate,JadwalUpdateNoImage]
api_ModelsDB = Jadwal
detail_identity = "jadwal"


#========================================================CRUD ROOM======================================================
@route_jadwal.post(api_address)
async def jadwal_add(user:user_refs,db:db_dependency, title: str = Form(...),content: str = Form(...),waktu_mulai: time = Form(...),tanggal_mulai: date=Form(...),pendeta_id:int=Form(...),category_id:int=Form(...),church_id:int=Form(...), file: UploadFile = File(...)):
    if not (title and file and content and waktu_mulai and tanggal_mulai and pendeta_id):
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
         db_input = api_ModelsDB(title= title,content= content, waktu_mulai=waktu_mulai, tanggal_mulai=tanggal_mulai, pendeta_id=pendeta_id,category_id=category_id,church_id=church_id, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_jadwal.put(api_address_long[0])
async def jadwal_update(user:user_refs,api_id:int,db:db_dependency, title: str = Form(...),content: str = Form(...),waktu_mulai: time = Form(...),tanggal_mulai: date=Form(...),pendeta_id:int=Form(...),category_id:int=Form(...),church_id:int=Form(...), file: UploadFile = File(...)):
    if not (title and file and content and waktu_mulai and tanggal_mulai and pendeta_id):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    if db_show.content_img != f'{Upload_Directory}{file.filename}':
        delete_temp = f'{db_show.jemaat_img}'
        if os.path.exists(delete_temp):
            os.remove(delete_temp)
            status_os = "Gambar Berubah"
        status_os = ""
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
         db_update= api_baseModelUpdate[0](title=title, content= content,waktu_mulai=waktu_mulai, tanggal_mulai=tanggal_mulai, pendeta_id=pendeta_id,category_id=category_id,church_id=church_id,content_img=path,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status
    return {"message": response }
@route_jadwal.put(api_address_long[1])
async def jadwal_update(user:user_refs,api_id:int,db:db_dependency, title: str = Form(...),content: str = Form(...),waktu_mulai: time = Form(...),tanggal_mulai: date=Form(...),pendeta_id:int=Form(...),category_id:int=Form(...),church_id:int=Form(...)):
    if not (title  and content and waktu_mulai and tanggal_mulai and pendeta_id):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    try:
        
         db_update= api_baseModelUpdate[1](title=title, content= content,waktu_mulai=waktu_mulai, tanggal_mulai=tanggal_mulai, pendeta_id=pendeta_id,category_id=category_id,church_id=church_id,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah"
    return {"message": response }

@route_jadwal.delete(api_address_long[0])
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

@route_jadwal.get(api_address_long[0])
async def jadwal_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    category = db_show.category
    church = db_show.church
    pendeta = db_show.pendeta
    color_id = category.color_id if category else None
    jadwal_dict ={
        "id" : db_show.id,
        "name" : db_show.title,
        "tanggal" : db_show.tanggal_mulai,
        'jam_mulai' : db_show.waktu_mulai,
        "content_img":db_show.content_img,
        "content": db_show.content,
        "category":{
            "id" :  category.id if category else None,
        },
        "church":{
            "id" :  church.id if church else None,
        },
        "pendeta":{
            "id" :  pendeta.id if pendeta else None,
        }    
    }
    return jadwal_dict

@route_jadwal.get(api_address)
async def jadwal_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    result = []
    for jadwal in db_show:
        category = jadwal.category
        church = jadwal.church
        pendeta = jadwal.pendeta
        color_id = category.color_id if category else None
        jadwal_dict ={
            "id" : jadwal.id,
            "name" : jadwal.title,
            "tanggal" : jadwal.tanggal_mulai,
            "content_img":jadwal.content_img,
            "content": jadwal.content,
            "category":{
                "name" :  category.name if category else None,
                "color_id": color_id
            },
            "church":{
                "name" :  church.name if church else None,
            },
            "pendeta":{
                "name" :  pendeta.name if pendeta else None,
                "pic" :  pendeta.profile_img if pendeta else None,
            }    
        }
        result.append(jadwal_dict)
    return result
