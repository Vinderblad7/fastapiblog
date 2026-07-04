from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Column, Integer, Text, DateTime, func, Table, ForeignKey
import datetime

post_tags_table = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


class TagsModel(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    posts: Mapped[list["PostModel"]] = relationship(
        secondary=post_tags_table,
        back_populates="tags"      
    )


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    tags: Mapped[list["TagsModel"]] = relationship(
        secondary=post_tags_table, 
        back_populates="posts"  
    )

    user: Mapped["UserModel"] = relationship(
    back_populates="posts",
    primaryjoin="PostModel.user_id == UserModel.id"
)