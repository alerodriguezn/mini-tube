from pydantic import BaseModel
# import file from fastapi
from fastapi import File, UploadFile

class VideosBase(BaseModel):
    title: str
    creationDate: str
    description: str
    video: UploadFile = File(...)
    thumbnail: UploadFile = File(...)

    class Config:
        orm_mode = True


class FavoriteVideosBase(BaseModel):
    videoId: int
    favoriteDate: str

    class Config:
        orm_mode = True


class CommentsBase(BaseModel):
    comment: str
    videoId: int

    class Config:
        orm_mode = True
