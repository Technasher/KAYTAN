from sqlalchemy import select
from DB.models.tg_user import TelegramUser
from DB.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    async def create(self, **kwargs) -> TelegramUser:
        user = TelegramUser(**kwargs)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> TelegramUser | None:
        stmt = select(TelegramUser).filter_by(telegram_id=telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_superuser_id_list(self):
        stmt = select(TelegramUser.telegram_id).filter_by(is_superuser=True)
        result = await self.session.execute(stmt)
        return result.scalars().all()
