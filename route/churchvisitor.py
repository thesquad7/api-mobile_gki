from datetime import date, datetime, time, timedelta
from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import ChurchVisitor,Jadwal
import config.upload
from sqlalchemy import select
from SchemasIndex import ChurchVUpdate,ChurchVRequest,ChurchVUpdatePUT
from .login import user_refs
import os
from config.setting import db_dependency

route_visitor= APIRouter(prefix="/admin", tags=['Visitor'])
route_visitor_public= APIRouter(prefix="", tags=['Public'])
api_id : str
api_address_long= "/visitor/{api_id}"
api_address = "/visitor/"
api_address_public = ["/p_visitor/","/p_visitor/{api_id}","/p_visitor_higlight/"]
api_address2 = "/visitor_jadwal/"
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
async def visitor_update(user:user_refs,api_id:int,db:db_dependency, body:ChurchVUpdatePUT):
    if not (body):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi " +detail_identity+ " tidak ditemukan")
    try:
         db_update= ChurchVUpdatePUT(**body.dict())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi " +detail_identity+ " telah berubah, "
    return {"message": response }

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
    jemaat_total = db_show.p_jemaat + db_show.w_jemaat
    visit_total = db_show.w_visit + db_show.p_visit
    total = jemaat_total + visit_total + (db_show.stream_count or 0)
    jadwal =db_show.jadwals
    category = jadwal.category
    pendeta = jadwal.pendeta
    church = jadwal.church
    db_show_dict = {
        "id": db_show.id,
        "w_jemaat": db_show.w_jemaat,
        "p_jemaat": db_show.p_jemaat,
        "w_visit": db_show.w_visit,
        "p_visit": db_show.p_visit,
        "stream_count": db_show.stream_count,
        "stream": db_show.stream,
        "jadwal":{
            'name' : jadwal.title if jadwal else None,
            'date' : jadwal.tanggal_mulai if jadwal else None,
            'jenis' : category.name if category else None,
            'pendeta' : pendeta.name if pendeta else None,\
            'file' : jadwal.content_img if jadwal else None,
            'p_pic' : pendeta.profile_img if pendeta else None,
            'place' : church.name if church else None,

        },
    }
    return db_show_dict

@route_visitor.get(api_address)
async def visitor_all(user:user_refs, db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if not (db_show) :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    result = []
    for visitor in db_show:
        jemaat_total = visitor.p_jemaat + visitor.w_jemaat
        visit_total = visitor.w_visit + visitor.p_visit
        total = jemaat_total + visit_total + (visitor.stream_count or 0)
        jadwal =visitor.jadwals
        category = jadwal.category
        pendeta = jadwal.pendeta
        church = jadwal.church
        visitor_dict = {
            "id": visitor.id,
            "jemaat_total": jemaat_total,
            "visit_total": visit_total,
            "created_at": visitor.created_at,
            "updated_at": visitor.updated_at,
            "stream_count": visitor.stream_count,
            "stream": visitor.stream,
            "total": total,
            "jadwal":{
                'id' : jadwal.id if jadwal else None,
                'name' : jadwal.title if jadwal else None,
                'date' : jadwal.tanggal_mulai if jadwal else None,
                'jenis' : category.name if category else None,
                'pendeta' : pendeta.name if pendeta else None,\
                'file' : jadwal.content_img if jadwal else None,
                'p_pic' : pendeta.profile_img if pendeta else None,
                'place' : church.name if church else None,

            },
        }
        result.append(visitor_dict)
    
    return result

@route_visitor.get(api_address2)
async def jadwal_for_visitor(user:user_refs, db:db_dependency):
    subquery = db.query(ChurchVisitor.jadwal_id).subquery()
    
    # Main query to get Jadwal entries not in the subquery
    db_show = db.query(Jadwal).filter(Jadwal.id.notin_(select(subquery.c.jadwal_id))).all()
    
    if not db_show:
        raise HTTPException(status_code=404, detail="Informasi jadwal belum tersedia")
    
    result = []
    for jadwal in db_show:
        category = jadwal.category
        church = jadwal.church
        pendeta = jadwal.pendeta
        color_id = category.color_id if category else None
        jadwal_dict = {
            "id": jadwal.id,
            "name": jadwal.title,
            "tanggal": jadwal.tanggal_mulai,
            "content_img": jadwal.content_img,
            "content": jadwal.content,
            "category": {
                "name": category.name if category else None,
                "color_id": color_id
            },
            "church": {
                "name": church.name if church else None,
            },
            "pendeta": {
                "name": pendeta.name if pendeta else None,
                "pic": pendeta.profile_img if pendeta else None,
            }
        }
        result.append(jadwal_dict)
    
    return result

@route_visitor_public.get(api_address_public[0])
async def visitor_all( db:db_dependency):
    db_show = db.query(api_ModelsDB).all()
    if not (db_show) :
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity+" belum tersedia")
    result = []
    for visitor in db_show:
        jemaat_total = visitor.p_jemaat + visitor.w_jemaat
        visit_total = visitor.w_visit + visitor.p_visit
        total = jemaat_total + visit_total + (visitor.stream_count or 0)
        jadwal =visitor.jadwals
        category = jadwal.category
        pendeta = jadwal.pendeta
        church = jadwal.church
        visitor_dict = {
            "id": visitor.id,
            "jemaat_total": jemaat_total,
            "visit_total": visit_total,
            "created_at": visitor.created_at,
            "updated_at": visitor.updated_at,
            "stream_count": visitor.stream_count,
            "stream": visitor.stream,
            "total": total,
            "jadwal":{
                'name' : jadwal.title if jadwal else None,
                'date' : jadwal.tanggal_mulai if jadwal else None,
                'jenis' : category.name if category else None,
                'pendeta' : pendeta.name if pendeta else None,\
                'file' : jadwal.content_img if jadwal else None,
                'p_pic' : pendeta.profile_img if pendeta else None,
                'place' : church.name if church else None,

            },
        }
        result.append(visitor_dict)
    
    return result
@route_visitor_public.get(api_address_public[1])
async def visitor_one(api_id:int, db:db_dependency):
    db_show = db.query(api_ModelsDB).filter(api_ModelsDB.id == api_id).first()
    jemaat_total = db_show.p_jemaat + db_show.w_jemaat
    visit_total = db_show.w_visit + db_show.p_visit
    total = jemaat_total + visit_total + (db_show.stream_count or 0)
    jadwal =db_show.jadwals
    category = jadwal.category
    pendeta = jadwal.pendeta
    church = jadwal.church
    db_show_dict = {
        "id": db_show.id,
        "w_jemaat": db_show.w_jemaat,
        "p_jemaat": db_show.p_jemaat,
        "w_visit": db_show.w_visit,
        "p_visit": db_show.p_visit,
        "jemaat_total": jemaat_total,
        "visit_total": visit_total,
        "total": total,
        "stream_count": db_show.stream_count,
        "stream": db_show.stream,
        "jadwal":{
            'name' : jadwal.title if jadwal else None,
            'date' : jadwal.tanggal_mulai if jadwal else None,
            'jenis' : category.name if category else None,
            'pendeta' : pendeta.name if pendeta else None,\
            'file' : jadwal.content_img if jadwal else None,
            'p_pic' : pendeta.profile_img if pendeta else None,
            'place' : church.name if church else None,

        },
    }
    return db_show_dict

@route_visitor_public.get(api_address_public[2])
async def visitor_all(db: db_dependency):
    one_week_ago = datetime.now() - timedelta(weeks=1)
    
    db_show = (
        db.query(api_ModelsDB)
        .filter(
            (api_ModelsDB.created_at >= one_week_ago) |
            (api_ModelsDB.updated_at >= one_week_ago)
        )
        .order_by(api_ModelsDB.created_at.desc())  # Sort by created_at, descending
        .limit(2)  # Limit results to 2
        .all()
    )
    
    if not db_show:
        raise HTTPException(status_code=404, detail="Informasi " + detail_identity + " belum tersedia")
    
    result = []
    for visitor in db_show:
        jemaat_total = visitor.p_jemaat + visitor.w_jemaat
        visit_total = visitor.w_visit + visitor.p_visit
        total = jemaat_total + visit_total + (visitor.stream_count or 0)
        jadwal = visitor.jadwals
        category = jadwal.category if jadwal else None
        pendeta = jadwal.pendeta if jadwal else None
        church = jadwal.church if jadwal else None
        visitor_dict = {
            "id": visitor.id,
            "jemaat_total": jemaat_total,
            "visit_total": visit_total,
            "created_at": visitor.created_at,
            "updated_at": visitor.updated_at,
            "stream_count": visitor.stream_count,
            "stream": visitor.stream,
            "total": total,
            "jadwal": {
                'name': jadwal.title if jadwal else None,
                'date': jadwal.tanggal_mulai if jadwal else None,
                'jenis': category.name if category else None,
                'pendeta': pendeta.name if pendeta else None,
                'file': jadwal.content_img if jadwal else None,
                'p_pic': pendeta.profile_img if pendeta else None,
                'place': church.name if church else None,
            },
        }
        result.append(visitor_dict)
    
    return result