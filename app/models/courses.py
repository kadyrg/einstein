from datetime import datetime, timezone
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from typing import TYPE_CHECKING

from .base import Base


if TYPE_CHECKING:
    from .chapters import Chapter

class Course(Base):
    __tablename__ = "courses"
    
    title: Mapped[str] = mapped_column(unique=True)
    image_path: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    chapters: Mapped[list["Chapter"]] = relationship(back_populates="course", cascade="all, delete-orphan")
