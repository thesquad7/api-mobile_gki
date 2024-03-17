from fastapi import HTTPException, UploadFile, APIRouter,Form,File
from ModelIndex import Pendeta
import config.upload
from models.categories import Category
from SchemasIndex import CategoryCreate
from .login import user_refs
from config.setting import db_dependency

route_category= APIRouter(prefix="/admin", tags=['Category'])

@route_category.post("/category/")
async def category_create(user:user_refs,name:CategoryCreate, db:db_dependency):
    db_input = Category(**name.dict())
    db.add(db_input)
    db.commit()
    db.close()
    return {"message": "Category telah di tambahkan"}

@route_category.put("/category/{api_id}")
async def visitor_update(user:user_refs,api_id:int,db:db_dependency, body:CategoryCreate):
    if not (body):
        raise HTTPException(status_code=400, detail="Semua form harus di isi")
    db_show = db.query(Category).filter(Category.id == api_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Informasi category tidak ditemukan")
    try:
         db_update= CategoryCreate(**body.dict())
         for field, value in db_update.dict(exclude_unset=True).items():
            setattr(db_show, field, value)
         db.commit()
         db.refresh(db_show)
    finally:
        db.close()
    response = "Informasi category telah berubah, "
    return {"message": response }
@route_category.delete("/category/{category_id}")
async def delete_category(user:user_refs,category_id: int, db:db_dependency):
    db_delete=db.query(Category).filter(Pendeta.id == category_id).first()
    if db_delete is None:
        raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")
    db.delete(db_delete)
    db.commit()
    return {"message": "Informasi Pendeta telah di hapus"}

@route_category.get("/category/{category_id}")
async def category_one(user:user_refs,category_id:int, db:db_dependency):
    db_show = db.query(Category).filter(Category.id == category_id).first()
    return db_show

@route_category.get("/category/")
async def category_show(user:user_refs, db:db_dependency):
    db_show = db.query(Category).all()
    return db_show