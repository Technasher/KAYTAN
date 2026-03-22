from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_deactivate_button(program_id) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text='Деактивировать',
        callback_data=f'deactivate:{program_id}'
    )


def get_deactivate_keyboard(program_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                get_deactivate_button(program_id)
            ]
        ]
    )
