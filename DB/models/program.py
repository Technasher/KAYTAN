from .base import Base
from typing import Optional
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


class Program(Base):
    __tablename__ = 'program'

    name: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)
