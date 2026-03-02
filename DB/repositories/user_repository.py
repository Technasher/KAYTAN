from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from DB.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).filter_by(telegram_id=telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_superuser_id_list(self):
        stmt = select(User.telegram_id).filter_by(is_superuser=True)
        result = await self.session.execute(stmt)
        return result.scalars().all()
