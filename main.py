from fastapi import FastAPI
from fastapi.responses import FileResponse
from config.db import engine, Base
from route.auth import route_auth
from route.login import route_login
from route.pendeta import route_pendeta
from route.church import route_gereja
from route.category import route_category
from route.jadwal import route_jadwal 
from route.kesaksian import route_kesakian
from route.churchvisitor import route_visitor
from route.acara import route_acara
from route.feedback import route_feedback
from route.moneymoons import route_money
from route.moneybank import route_tfmoney
from route.office import route_jamkerja
from route.jemaat import route_jemaat
app=FastAPI(title="GKI RESTful APIs")
Base.metadata.create_all(bind=engine)


app.include_router(router=route_auth)
app.include_router(router=route_login)  
app.include_router(router=route_pendeta)
app.include_router(router=route_category)
app.include_router(router=route_gereja)
app.include_router(router=route_jadwal)
app.include_router(router=route_kesakian)
app.include_router(router=route_visitor)
app.include_router(router=route_acara)
app.include_router(router=route_feedback)
app.include_router(router=route_money)
app.include_router(router=route_tfmoney)
app.include_router(router=route_jamkerja)
app.include_router(router=route_jemaat)
#app.include_router(router=route)
@app.get("/", response_class=FileResponse)
async def image(path_p: str):
    file_f = f"{path_p}"
    return FileResponse(file_f)


# @app.post("/jadwal",status_code=status.HTTP_201_CREATED)
# async def create_jadwal(title_i: str, content_i:str,tanggal_mulai_i:date, waktu_mulai_i:time,pendeta_id_i:str, file: UploadFile, db: db_dependency):
#     path = f'{config.upload.JADWAL_IMG_DIR}{file.filename}'
#     with open(path, "wb") as buffer:
#         buffer.write(await file.read())
#     db_jadwal= ModelIndex.Jadwal(title = title_i, content = content_i,tanggal_mulai=tanggal_mulai_i,waktu_mulai= waktu_mulai_i,pendeta_id=pendeta_id_i,content_img=path )
#     db.add(db_jadwal)
#     db.commit()
#     return{"detail": "Jadwal di upload"}

# @app.get("/jadwal/{jadwal_id}", status_code=status.HTTP_200_OK)
# async def read_jadwal(jadwal_id: int, db : db_dependency):
#     jadwal=db.query(ModelIndex.Jadwal).filter(ModelIndex.Jadwal == jadwal_id).first
#     if jadwal is None:
#         raise HTTPException(status_code=404, detail="Jadwal Tidak Ditemukan")
#     return jadwal


# @app.delete("/jadwal/{jadwal_id}", status_code=status.HTTP_200_OK)
# async def delete_jadwal(jadwal_id: int, db:db_dependency):
#     db_jadwal=db.query(ModelIndex.Jadwal).filter(ModelIndex.Jadwal.id).first()
#     if jadwal_id is None:
#         raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")
#     db.delete(db_jadwal)
#     db.commit()

# @app.post("/users/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: schemas.index.User, db: db_dependency):
#     db_user= models.ModelIndex.User(**user.dict())
#     db.add(db_user)
#     db.commit()

# @app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
# async def read_user(user_id: int, db: db_dependency):
#     user = db.query (models.ModelIndex.User).filter(models.ModelIndex.User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User Tidak Ditemukan")
#     return user
