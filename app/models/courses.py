from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base


if TYPE_CHECKING:
    from .chapters import Chapter

class Course(Base):
    __tablename__ = "courses"
    
    title: Mapped[str] = mapped_column(unique=True)
    image_path: Mapped[str]

    chapters: Mapped[list["Chapter"]] = relationship(back_populates="course", cascade="all, delete-orphan")
