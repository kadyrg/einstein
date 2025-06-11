from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, DateTime
from typing import TYPE_CHECKING
from datetime import datetime, timezone

from .base import Base


if TYPE_CHECKING:
    from .courses import Course

class Chapter(Base):
    __tablename__ = 'chapters'

    title: Mapped[str]
    video_path: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="chapters")
