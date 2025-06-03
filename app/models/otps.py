from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime, timezone

from .base import Base


class OTP(Base):
    __tablename__ = "otps"

    email: Mapped[str]
    code: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    use_count: Mapped[int] = mapped_column(default=0)
    is_used: Mapped[bool] = mapped_column(default=False)
