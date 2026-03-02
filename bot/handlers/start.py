from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from DB.repositories.program_repository import ProgramRepository
from DB.repositories.user_repository import UserRepository

from bot.keyboards.InlineProgramList import get_inline_active_program_list

router = Router()


@router.message(Command("start"))
async def start(message: types.Message, session: AsyncSession):
    user_repo = UserRepository(session)
    program_repo = ProgramRepository(session)
    programs = await program_repo.get_active_list()
    # Проверяем, есть ли пользователь в БД
    user = await user_repo.get_by_telegram_id(message.from_user.id)

    if not user:
        user = await user_repo.create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        await message.answer(
            f"👋 Привет, {message.from_user.first_name}!\n"
            f"TODO: Приветственное сообщение"
        )
    else:
        await message.answer(
            f"С возвращением, {message.from_user.first_name}!"
        )

    keyboard = await get_inline_active_program_list(programs)
    await message.answer(
        'TODO: Сообщение со списком активных программ',
        reply_markup=keyboard
    )
