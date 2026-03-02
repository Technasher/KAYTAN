from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from DB.repositories.user_repository import UserRepository


class MessageAdminFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        telegram_id = message.from_user.id
        user_repo = UserRepository(session)
        superuser_id_list = await user_repo.get_superuser_id_list()
        return telegram_id in superuser_id_list


class CallbackAdminFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, session: AsyncSession) -> bool:
        telegram_id = callback.message.chat.id
        user_repo = UserRepository(session)
        superuser_id_list = await user_repo.get_superuser_id_list()
        return telegram_id in superuser_id_list
