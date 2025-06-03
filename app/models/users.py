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
    
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    type: Mapped[UserType] = mapped_column(SqlEnum(UserType), default=UserType.student)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
