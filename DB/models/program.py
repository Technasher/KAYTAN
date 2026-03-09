from .base import Base
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .telegram_media import TelegramMedia


class Program(Base):
    __tablename__ = 'program'

    name: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)

    telegram_media: Mapped[List['TelegramMedia']] = relationship(secondary='program_telegram_media', back_populates='program')

    # telegram_media_associations: Mapped[List['ProgramTelegramMedia']] = relationship(back_populates='program')