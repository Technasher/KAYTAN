from aiogram import Router, F
from aiogram.types import CallbackQuery
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
    await callback.message.answer(
        program.description,
        reply_markup=await get_deactivate_kb(program_id) if is_admin else None
    )