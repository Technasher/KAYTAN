from typing import Optional

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class TelegramUser(Base):
    __tablename__ = 'telegram_user'

    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    # phone_number: Mapped[str] = mapped_column(nullable=True)

    is_superuser: Mapped[bool] = mapped_column(default=False)
