from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_deactivate_kb(program_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Деактивировать',
                    callback_data=f'deactivate:{program_id}'
                )
            ]
        ]
    )
