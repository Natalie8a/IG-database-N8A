from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date
from datetime import date
from typing import List
from sqlalchemy import String, Boolean, Integer, ForeignKey, Date, Enum
import enum

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    # relaciones User one to many
    say: Mapped[List["Post"]] = relationship(back_populates="author")
    reply: Mapped[List["Comment"]] = relationship(back_populates="author")
    photo: Mapped[List["Media"]] = relationship(back_populates="author")
    track: Mapped[List["Follow"]] = relationship(back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    __tablebame__ = "post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    date: Mapped[str] = mapped_column(Date, default=date.today)
    message: Mapped[str] = mapped_column(String(400), nullable=False)
    # relaciones Post one to many
    reply: Mapped[List["Comment"]] = relationship(back_populates="say")
    photo: Mapped[List["Media"]] = relationship(back_populates="say")
    # relación many to one
    author: Mapped["User"] = relationship(back_populates="say")

    def serialize(self):
        return {
            "id": self.id,
            'user_id': self.user_id,
            "date": self.date,
            "message": self.message,
        }


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(400), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))

    say: Mapped["Post"] = relationship(back_populates="reply")
    author: Mapped["User"] = relationship(back_populates="reply")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "user_id": self.user_id,
            "post_id": self.post_id,

        }


# class MediaType(enum.Enum):
#     IMAGE = "image"
#     VIDEO = "video"
#     Audio = "audio"


class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    Post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    # relaciones
    author: Mapped["User"] = relationship(back_populates="photo")
    say: Mapped["Post"] = relationship(back_populates="photo")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "user_id": self.user_id,
            "post_id": self.Post_id,
        }


class Follow(db.Model):
    __tablename__ = "follow"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_from_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user_to_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))

    # relationships
    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
