from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from DB.repositories.program_repository import ProgramRepository
from bot.filters.admin import MessageAdminFilter, CallbackAdminFilter
from bot.keyboards.DeactivateProgramInline import get_deactivate_kb

router = Router()
router.callback_query.filter(F.data.startswith("program:"))


@router.callback_query()
async def program_user(callback: CallbackQuery, session: AsyncSession):
    program_repo = ProgramRepository(session)
    program_id = int(callback.data.split(":")[1])
    program = await program_repo.get_program_by_id(program_id)
    admin_filter = CallbackAdminFilter()
    is_admin = await admin_filter(callback, session)
    if program.telegram_media:
        media_group = MediaGroupBuilder()
        media_group.add(
            type=program.telegram_media[0].file_type.to_str(),
            media=program.telegram_media[0].file_id,
            caption=program.description
        )
        for media in program.telegram_media[1:]:
            media_group.add(type=media.file_type.to_str(), media=media.file_id)
        await callback.message.answer_media_group(media=media_group.build())
    else:
        await callback.message.answer(program.description)
    if is_admin:
        await callback.message.answer(
            'Что хотите сделать с данной программой?',
            reply_markup=await get_deactivate_kb(program_id) if is_admin else None
        )

