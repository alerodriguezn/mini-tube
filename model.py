from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date
from sqlalchemy.orm import relationship

from database import Base


class Videos(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    creationDate = Column(Date)
    description = Column(String)
    videoPath = Column(String)
    thumbnailPath = Column(String)
    viewsCount = Column(Integer)
    
    comments = relationship("Comments", back_populates="video")
    favoriteVideos = relationship("FavoriteVideos", back_populates="video")



class FavoriteVideos(Base):
    __tablename__ = "favoriteVideos"

    id = Column(Integer, primary_key=True)
    videoId = Column(Integer, ForeignKey("videos.id"))
    favoriteDate = Column(Date)
    video = relationship("Videos", back_populates="favoriteVideos")


class Comments (Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment = Column(String)
    videoId = Column(Integer, ForeignKey("videos.id"))
    video = relationship("Videos", back_populates="comments")