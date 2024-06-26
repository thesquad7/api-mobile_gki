from datetime import date, datetime, time,timedelta
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Acara
import config.upload
from SchemasIndex import AcaraUpdate,AcaraCreate,AcaraUpdateNoImage
from .login import user_refs
import os
from PIL import Image
from config.setting import db_dependency

route_acara= APIRouter(prefix="/admin", tags=['Acara'])
route_acara_public= APIRouter(prefix="", tags=['Public'])
api_id : str
api_address_long= "/acara/{api_id}"
api_address_long2= "/acara_no_image/{api_id}"
api_address = "/acara/"
api_address_public = ["/p_acara/","/p_acara/{api_id}","/p_acara_highlight/"]
Upload_Directory = config.upload.ACARA_IMG_DIR
api_baseModelCreate = AcaraCreate
api_baseModelUpdate = [AcaraUpdate, AcaraUpdateNoImage]
api_ModelsDB = Acara
detail_identity = "acara"


#========================================================CRUD ROOM======================================================
@route_acara.post(api_address)
async def acara_add(user:user_refs,db:db_dependency, name: str = Form(...),content: str = Form(...),status:str= Form(...),jam_acara:time =Form(...),location:str= Form(...),tanggal: date=Form(...),category_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and file and content and  tanggal and category_id and status):
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

         db_input = api_ModelsDB(name= name,content= content,jam_acara = jam_acara, tanggal=tanggal,location=location, category_id=category_id,status=status, content_img=path)
         db.add(db_input)
         db.commit()
    finally:
        db.close()
    return {"message": detail_identity +" telah di tambahkan"}

@route_acara.put(api_address_long)
async def acara_update(user:user_refs,api_id:int,db:db_dependency, name: str = Form(...),jam_acara:time =Form(...),status:str= Form(...),content: str = Form(...),tanggal: date=Form(...),category_id:int=Form(...), file: UploadFile = File(...)):
    if not (name and file and content and tanggal and status and category_id):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    status_os = ""
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    if db_show.content_img != f'{Upload_Directory}{file.filename}':
        delete_temp = f'{db_show.content_img}'
        if os.path.exists(delete_temp):
            os.remove(delete_temp)
            status_os = "Photo Berubah"
        
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

         db_update= api_baseModelUpdate[0](name=name, content= content,jam_acara = jam_acara, tanggal=tanggal,status=status, category_id=category_id,content_img=path,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, " +status_os
    return {"message": response }

@route_acara.put(api_address_long2)
async def acara_update(user:user_refs,api_id:int,db:db_dependency, name: str = Form(...),jam_acara:time =Form(...),status:str= Form(...),content: str = Form(...),tanggal: date=Form(...),category_id:int=Form(...)):
    if not (name and content and tanggal and status and category_id):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()    
    try:
         db_update= api_baseModelUpdate[1](name=name, content= content,jam_acara = jam_acara, tanggal=tanggal,status=status, category_id=category_id,updated_at=datetime.now())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah" 
    return {"message": response }

@route_acara.delete(api_address_long)
async def delete_acara(user:user_refs,api_id: int, db:db_dependency):
    db_delete=db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    os_delete_status = ""
    if db_delete is None:
        raise HTTPException(status_code=404, detail="Informasi "+detail_identity+" tidak ditemukan")
    delete_temp = f'{db_delete.content_img}'
    if os.path.exists(delete_temp):
        os.remove(delete_temp)
        os_delete_status = "Gambar di Hapus"
    
    db.delete(db_delete)
    db.commit()
    response = "Informasi "+detail_identity+ " telah di hapus," + os_delete_status
    return {"message": response}

@route_acara.get(api_address_long)
async def acara_one(user:user_refs,api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    modified_response = {'id': db_show.id,'location' : db_show.location, 'name': db_show.name, 'content':db_show.content, 'tanggal':db_show.tanggal,'jam_mulai':db_show.jam_acara, 'category_id': db_show.category_id,'status':db_show.status, 'content_img': db_show.content_img}
    return modified_response

@route_acara.get(api_address)
async def acara_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    result = []
    for acara in db_show:
        category = acara.category
        color_id = category.color_id if category else None
        acara_dict ={
            "id" : acara.id,
            "name" : acara.name,
            "status" : acara.status,
            "content_img":acara.content_img,
            "content": acara.content,
            "location": acara.location,
            "tanggal": acara.tanggal,
            "jam_acara": acara.jam_acara,
            "category":{
                "id": category.id if category else None,
                "name" :  category.name if category else None,
                "color_id": color_id
            }
            
        }
        result.append(acara_dict)
    return result

@route_acara_public.get(api_address_public[1])
async def acara_one(api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    category = db_show.category
    modified_response = {'id': db_show.id,'location' : db_show.location, 'name': db_show.name, 'content':db_show.content, 'tanggal':db_show.tanggal,'jam_mulai':db_show.jam_acara, 'category_name': category.name,'status':db_show.status, 'content_img': db_show.content_img}
    return modified_response

@route_acara_public.get(api_address_public[0])
async def acara_all( db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if db_show is None or "" :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    result = []
    for acara in db_show:
        category = acara.category
        color_id = category.color_id if category else None
        acara_dict ={
            "id" : acara.id,
            "name" : acara.name,
            "status" : acara.status,
            "content_img":acara.content_img,
            "content": acara.content,
            "location": acara.location,
            "tanggal": acara.tanggal,
            "jam_acara": acara.jam_acara,
            "category":{
                "name" :  category.name if category else None,
                "color_id": color_id
            }
            
        }
        result.append(acara_dict)
    return result
@route_acara_public.get(api_address_public[2])
async def acara_all(db: db_dependency):
    three_weeks_ago = datetime.now() - timedelta(weeks=3)
    
    db_show = (
        db.query(api_ModelsDB)
        .filter(
            (api_ModelsDB.created_at >= three_weeks_ago) |
            (api_ModelsDB.updated_at >= three_weeks_ago)
        )
        .order_by(api_ModelsDB.created_at.desc())  # Sort by created_at, descending
        .limit(4)  # Limit results to 4
        .all()
    )
    
    if not db_show:
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity + " belum tersedia")
    
    result = []
    for acara in db_show:
        category = acara.category
        color_id = category.color_id if category else None
        acara_dict = {
            "id": acara.id,
            "name": acara.name,
            "status": acara.status,
            "content_img": acara.content_img,
            "content": acara.content,
            "location": acara.location,
            "tanggal": acara.tanggal,
            "jam_acara": acara.jam_acara,
            "category": {
                "name": category.name if category else None,
                "color_id": color_id
            }
        }
        result.append(acara_dict)
    
    return result