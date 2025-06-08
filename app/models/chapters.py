from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

from sqlalchemy.testing.schema import mapped_column

from .base import Base


if TYPE_CHECKING:
    from .courses import Course

class Chapter(Base):
    __tablename__ = 'chapters'

    title: Mapped[str]
    image_path: Mapped[str]

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="chapters")
