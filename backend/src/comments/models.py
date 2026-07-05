from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Column, Integer, Text, DateTime, func, Table, ForeignKey
import datetime

class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    post: Mapped["PostModel"] = relationship(
    back_populates="comments",
    )

    user: Mapped["UserModel"] = relationship(
    back_populates="comments",
    )