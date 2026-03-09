from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DB.models.base import Base

if TYPE_CHECKING:
    from DB.models.program import Program
    from DB.models.telegram_media import TelegramMedia


class ProgramTelegramMedia(Base):
    __tablename__ = 'program_telegram_media'

    program_id: Mapped[int] = mapped_column(ForeignKey('program.id'), primary_key=True)
    telegram_media_id: Mapped[int] = mapped_column(ForeignKey('telegram_media.id'), primary_key=True)
