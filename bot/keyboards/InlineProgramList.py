from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from DB.repositories.program_repository import ProgramRepository


async def get_inline_active_program_list(programs: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for program in programs:
        builder.button(
            text=program.name,
            callback_data=f'program:{program.id}'
        )
    builder.adjust(1)
    return builder.as_markup()
