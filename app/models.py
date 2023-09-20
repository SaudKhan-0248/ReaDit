from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import List, Literal


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[List["Post"]] = relationship(
        "Post", backref="user", cascade="all, delete-orphan")
    votes: Mapped[List['Vote']] = relationship(
        "Vote", backref="user", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", backref="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(default=datetime.today())
    owner_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    votes: Mapped[List['Vote']] = relationship(
        "Vote", backref="post", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", backref="post", cascade="all, delete-orphan")


class Vote(Base):
    __tablename__ = 'votes'

    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    value: Mapped[Literal["1", "-1"]] = mapped_column(nullable=False)


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey(
        "posts.id", ondelete="CASCADE"), nullable=False)


class RevokedToken(Base):
    __tablename__ = 'revoked_token'

    id: Mapped[int] = mapped_column(primary_key=True)
    revtoken: Mapped[str] = mapped_column(unique=True)
