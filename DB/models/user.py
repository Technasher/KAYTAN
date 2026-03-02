from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = 'user'

    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str]
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    # phone_number: Mapped[str] = mapped_column(nullable=True)

    is_superuser: Mapped[bool] = mapped_column(default=False)
