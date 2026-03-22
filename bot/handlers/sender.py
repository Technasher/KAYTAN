from aiogram import types, Router, F, Bot
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from DB.repositories.program_repository import ProgramRepository
from DB.repositories.user_repository import UserRepository

router = Router()


@router.callback_query(F.data.startswith('send_all:'))
async def sender(callback: types.CallbackQuery, session: AsyncSession, bot: Bot):
    program_repo = ProgramRepository(session)
    program_id = int(callback.data.split(':')[1])
    program = await program_repo.get_program_by_id(program_id)

    user_repo = UserRepository(session)
    user_list = await user_repo.user_list
    # user_count = len(user_list)

    await callback.message.answer('Запуск рассылки')
    # progress_message = await callback.message.answer(f'0/{user_count}')

    if program.telegram_media:
        media_group = MediaGroupBuilder()
        media_group.add(
            type=program.telegram_media[0].file_type.to_str(),
            media=program.telegram_media[0].file_id,
            caption=program.description
        )
        for media in program.telegram_media[1:]:
            media_group.add(type=media.file_type.to_str(), media=media.file_id)

        for user in user_list:
            await bot.send_media_group(user.telegram_id, media_group.build())
    else:
        for user in user_list:
            await bot.send_message(user.telegram_id, program.description)

    await callback.message.answer('Рассылка завешена')
