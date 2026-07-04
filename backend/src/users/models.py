from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Column, Integer, Text, DateTime, func, Table, ForeignKey
import datetime

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    posts: Mapped[list["PostModel"]] = relationship(
    back_populates="user", 
    cascade="all, delete-orphan",
    primaryjoin="UserModel.id == PostModel.user_id"
    )