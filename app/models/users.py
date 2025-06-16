from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SqlEnum, DateTime
from enum import Enum
from datetime import datetime, timezone

from .base import Base


class UserType(str, Enum):
    admin = "admin",
    student = "student"


class User(Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)

    type: Mapped[UserType] = mapped_column(SqlEnum(UserType), nullable=False, default=UserType.student)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
