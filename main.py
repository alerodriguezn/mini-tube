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
