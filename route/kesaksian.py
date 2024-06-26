from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Kesaksian,Jemaats,Pendeta
import config.upload
from SchemasIndex import KesaksianUpdate,KesaksianCreate, ProfileBase
from .login import user_refs
import os
from datetime import date, datetime
from config.setting import db_dependency
from PIL import Image
from typing import List

route_kesakian= APIRouter(prefix="/admin", tags=['Kesaksian'])
route_kesaksian_public= APIRouter(prefix="", tags=['Public'])
api_id : str
api_address_long= "/kesaksian/{api_id}"
api_address = "/kesaksian/"
api_address_public = ["/p_kesaksian/","/p_kesaksian/{api_id}"]
api_address2 = "/kesaksian_author/"
Upload_Directory = config.upload.KESAKSIAN_IMG_DIR
api_baseModelCreate = KesaksianCreate
api_baseModelUpdate = KesaksianUpdate
api_ModelsDB = Kesaksian
api_ConnectModels1 = Jemaats
api_ConnectModels2 = Pendeta
detail_identity = "kesaksian"


#========================================================CRUD ROOM======================================================
@route_kesakian.post(api_address)
async def jadwal_add(user:user_refs,db:db_dependency, name: str = Form(...),date:date=Form(...),author: str = Form(...),user_id:int=Form(...),content: str = Form(...), file: UploadFile = File(...)):
    if not (name and author and file and user_id and date):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    
    try:
         path = f'{Upload_Directory}{file.filename}'
         with open(path, "wb") as buffer:
            buffer.write(await file.read())
         db_input = api_ModelsDB(name= name,author= author,user_id=user_id,date=date,content=content, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_kesakian.put(api_address_long)
async def jadwal_update(user:user_refs,api_id:int,db:db_dependency, name: str = Form(...),date:date = Form(...),author: str = Form(...),content: str = Form(...),user_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and file and status and user_id and date):
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
         path = os.path.join(Upload_Directory, file.filename)
         temp_path = os.path.join(Upload_Directory, f"temp_{file.filename}")
        
         with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
            
         with Image.open(temp_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(path, "JPEG", optimize=True, quality=70)

         os.remove(temp_path)
         db_update= api_baseModelUpdate(name=name, author= author,user_id=user_id, date=date,content=content,content_img=path,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status
    return {"message": response }
@route_kesakian.put(api_address_long)
async def jadwal_update_no_image(user:user_refs,api_id:int,db:db_dependency, name: str = Form(...),date:date = Form(...),author: str = Form(...),content: str = Form(...),user_id:int=Form(...)):
    if not (name and user_id and date):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    try:
         db_update= api_baseModelUpdate(name=name, author= author,user_id=user_id, date=date,content=content,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah"
    return {"message": response }

@route_kesakian.delete(api_address_long)
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

@route_kesakian.get(api_address_long)
async def jadwal_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    user_info= []
    jemaat_profile = db.query(api_ConnectModels1.id, api_ConnectModels1.profile_img, api_ConnectModels1.name).filter(api_ConnectModels1.id == db_show.user_id,api_ConnectModels1.name == db_show.author).first()
    if jemaat_profile:
        user_info = {
            "id": jemaat_profile.id,
            "name": jemaat_profile.name
    }
    pendeta_profile = db.query(api_ConnectModels2.id, api_ConnectModels2.profile_img, api_ConnectModels2.name).filter(api_ConnectModels2.id == db_show.user_id,api_ConnectModels2.name == db_show.author).first()
    if pendeta_profile:
        user_info ={
            "id": pendeta_profile.id,
            "name": pendeta_profile.name
    }
    kesaksian_dict ={
        "id" : db_show.id,
        "name" : db_show.name,
        "tanggal" : db_show.date,
        "content_img":db_show.content_img,
        "content": db_show.content,
        "user" : user_info
        }
    return kesaksian_dict

@route_kesakian.get(api_address2,response_model=List[ProfileBase])
async def author_kesaksian(user:user_refs, db:db_dependency):
    jemaats_profiles = db.query(api_ConnectModels1.id, api_ConnectModels1.profile_img, api_ConnectModels1.name).all()
    pendeta_profiles = db.query(api_ConnectModels2.id, api_ConnectModels2.profile_img, api_ConnectModels2.name).all()
    if jemaats_profiles and pendeta_profiles  is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    profiles = jemaats_profiles + pendeta_profiles
    return profiles

@route_kesakian.get(api_address)
async def jadwal_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    result = []
    for kesaksian in db_show:
        user_info= None
        jemaat_profile = db.query(api_ConnectModels1.id, api_ConnectModels1.profile_img, api_ConnectModels1.name).filter(api_ConnectModels1.id == kesaksian.user_id,api_ConnectModels1.name == kesaksian.author).first()
        if jemaat_profile:
            user_info ={
                "id": jemaat_profile.id,
                "profile_img": jemaat_profile.profile_img,
                "name": jemaat_profile.name
        }
        pendeta_profile = db.query(api_ConnectModels2.id, api_ConnectModels2.profile_img, api_ConnectModels2.name).filter(api_ConnectModels2.id == kesaksian.user_id,api_ConnectModels2.name == kesaksian.author).first()
        if pendeta_profile:
            user_info ={
                "id": pendeta_profile.id,
                "profile_img": pendeta_profile.profile_img,
                "name": pendeta_profile.name
        }
        kesaksian_dict ={
            "id" : kesaksian.id,
            "name" : kesaksian.name,
            "tanggal" : kesaksian.date,
            "content_img":kesaksian.content_img,
            "content": kesaksian.content,
            "user" : {
                'name' : user_info["name"],
                'id' : user_info["id"],
                'profile_img' : user_info["profile_img"],
            }
        }
        result.append(kesaksian_dict)
    return result

@route_kesaksian_public.get(api_address_public[0])
async def jadwal_all(db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    result = []
    for kesaksian in db_show:
        user_info= None
        jemaat_profile = db.query(api_ConnectModels1.id, api_ConnectModels1.profile_img, api_ConnectModels1.name).filter(api_ConnectModels1.id == kesaksian.user_id,api_ConnectModels1.name == kesaksian.author).first()
        if jemaat_profile:
            user_info ={
                "profile_img": jemaat_profile.profile_img,
                "name": jemaat_profile.name
        }
        pendeta_profile = db.query(api_ConnectModels2.id, api_ConnectModels2.profile_img, api_ConnectModels2.name).filter(api_ConnectModels2.id == kesaksian.user_id,api_ConnectModels2.name == kesaksian.author).first()
        if pendeta_profile:
            user_info ={
                "profile_img": pendeta_profile.profile_img,
                "name": pendeta_profile.name
        }
        kesaksian_dict ={
            "id" : kesaksian.id,
            "name" : kesaksian.name,
            "tanggal" : kesaksian.date,
            "content_img":kesaksian.content_img,
            "content": kesaksian.content,
            "user" : {
                'name' : user_info["name"],
                'profile_img' : user_info["profile_img"],
            }
        }
        result.append(kesaksian_dict)
    return result

@route_kesaksian_public.get(api_address_public[1])
async def jadwal_one(api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    user_info= []
    jemaat_profile = db.query(api_ConnectModels1.id, api_ConnectModels1.profile_img, api_ConnectModels1.name).filter(api_ConnectModels1.id == db_show.user_id,api_ConnectModels1.name == db_show.author).first()
    if jemaat_profile:
        user_info = {
            "name": jemaat_profile.name,
            "pic" : jemaat_profile.profile_img
    }
    pendeta_profile = db.query(api_ConnectModels2.id, api_ConnectModels2.profile_img, api_ConnectModels2.name).filter(api_ConnectModels2.id == db_show.user_id,api_ConnectModels2.name == db_show.author).first()
    if pendeta_profile:
        user_info ={
            "name": pendeta_profile.name,
            "pic" : pendeta_profile.profile_img
    }
    kesaksian_dict ={
        "name" : db_show.name,
        "tanggal" : db_show.date,
        "content_img":db_show.content_img,
        "content": db_show.content,
        "user" : user_info
        }
    return kesaksian_dict