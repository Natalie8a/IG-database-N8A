from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date
from datetime import date
from sqlalchemy import String, Boolean, Integer, ForeignKey, Date, Enum
import enum

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    date: Mapped[str] = mapped_column(Date, default=date.today)
    message: Mapped[str] = mapped_column(String(400), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            'user_id': self.user_id,
            "date": self.date,
            "message": self.message,
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(400), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "user_id": self.user_id,
            "post_id": self.post_id,

        }


class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    Audio = "audio"


class Media(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
        }

class Follow(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_from_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user_to_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))

    def serialize(self):
        return{
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }