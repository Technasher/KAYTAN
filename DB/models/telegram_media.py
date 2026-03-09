from enum import Enum
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum as SQLAEnum

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .program import Program


class MediaType(Enum):
    PHOTO = 'photo'
    VIDEO = 'video'

    def to_str(self):
        return self._value_


class TelegramMedia(Base):
    __tablename__ = 'telegram_media'

    file_id: Mapped[str] = mapped_column(unique=True, index=True)
    file_unique_id: Mapped[str] = mapped_column(unique=True)
    file_type: Mapped[SQLAEnum] = mapped_column(SQLAEnum(MediaType))

    program: Mapped[List['Program']] = relationship(secondary='program_telegram_media', back_populates='telegram_media')

    # program_associations: Mapped[List['ProgramTelegramMedia']] = relationship(back_populates='telegram_media')
