import os
from typing import Union
from fastapi import FastAPI
from fastapi import Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import model
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from schemas import VideosBase

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

#Servicio web tipo GET para retornar los 10 videos más vistos. 

@app.get("/get-most-viewed/")
def get_most_viewed(db: Session = Depends(get_db)):
    videos = db.query(model.Videos).order_by(model.Videos.viewsCount.desc()).limit(10).all()
    return JSONResponse(content={"videos": videos}, status_code=200)

#Servicio web tipo GET para retornar los 10 videos favoritos más recientes.
#Este de acá abajo dice que obtiene los 10 videos más recientes, no los 10 favoritos más recientes.

@app.get("/get-most-recent/")
def get_most_recent(db: Session = Depends(get_db)):
    videos = db.query(model.Videos).order_by(model.Videos.creationDate.desc()).limit(10).all()
    return JSONResponse(content={"videos": videos}, status_code=200)




@app.post("/add-video/")
async def add_video(
    title: str = Form(...),
    description: str = Form(...),
    creationDate: str = Form(...),
    video: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    video_content = await video.read()
    thumbnail_content = await thumbnail.read()

    try:
        with open(f"data/videos/{video.filename}", "wb") as fv:
            fv.write(video_content)

        with open(f"data/thumbnails/{thumbnail.filename}", "wb") as ft:
            ft.write(thumbnail_content)

        db_video = model.Videos(
            title=title,
            creationDate=creationDate,
            description=description,
            videoPath=f"data/videos/{video.filename}",
            thumbnailPath=f"data/thumbnails/{thumbnail.filename}",
            viewsCount=0,
        )

        db.add(db_video)
        db.commit()
        db.refresh(db_video)

        return JSONResponse(
            content={"message": "File saved successfully"}, status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"message": "File could not be saved"}, status_code=400
        )
        

#Servicio web tipo GET para buscar videos en la base de datos. 

@app.get("/get-videos/")
def get_videos(db: Session = Depends(get_db)):
    videos = db.query(model.Videos).all()
    return JSONResponse(content={"videos": videos}, status_code=200)

#Servicio web tipo GET para cargar un video y sus datos (dependiendo de la implementación podrían ser dos servicios web separados).

@app.get("/get-video/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(model.Videos).filter(model.Videos.id == video_id).first()
    return JSONResponse(content={"video": video}, status_code=200)



@app.put("/increase-view-count/{video_id}")
def increase_view_count(video_id: int, db: Session = Depends(get_db)):
    video = db.query(model.Videos).filter(model.Videos.id == video_id).first()
    video.viewsCount += 1
    db.commit()
    return JSONResponse(content={"message": "View count increased"}, status_code=200)

#Servicio web tipo PUT para agregar un video a los favoritos.

@app.put("/add-to-favorites/{video_id}")
def add_to_favorites(video_id: int, db: Session = Depends(get_db)):
    video = db.query(model.Videos).filter(model.Videos.id == video_id).first()
    video.isFavorite = True
    db.commit()
    return JSONResponse(content={"message": "Video added to favorites"}, status_code=200)

#Servicio web tipo DELETE para quitar un video de los favoritos. 

@app.delete("/remove-from-favorites/{video_id}")
def remove_from_favorites(video_id: int, db: Session = Depends(get_db)):
    video = db.query(model.Videos).filter(model.Videos.id == video_id).first()
    video.isFavorite = False
    db.commit()
    return JSONResponse(content={"message": "Video removed from favorites"}, status_code=200)

#Servicio web tipo GET para cargar la lista de comentarios de un video. 

@app.get("/get-comments/{video_id}")
def get_comments(video_id: int, db: Session = Depends(get_db)):
    comments = db.query(model.Comments).filter(model.Comments.videoId == video_id).all()
    return JSONResponse(content={"comments": comments}, status_code=200)

#Servicio web tipo POST para agregar un comentario a un video.

@app.post("/add-comment/")
def add_comment(comment: str = Form(...), videoId: int = Form(...), db: Session = Depends(get_db)):
    db_comment = model.Comments(comment=comment, videoId=videoId)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return JSONResponse(content={"message": "Comment added successfully"}, status_code=200)
