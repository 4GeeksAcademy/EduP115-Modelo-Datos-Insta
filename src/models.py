from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum


class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3


db = SQLAlchemy()


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(15), nullable=False)
    lastname: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    type: Mapped[MyEnum] = mapped_column(Enum(MyEnum))
    url: Mapped[str] = mapped_column()
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship("Post", back_populates="media")


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
    media: Mapped[List["Media"]] = relationship("Media", back_populates="post")


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    comment_text: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         # do not serialize the password, its a security breach
    #     }
