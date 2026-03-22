from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_sender_keyboard(message_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                get_sender_button(message_id)
            ]
        ]
    )


def get_sender_button(program_id) -> InlineKeyboardButton:
    return InlineKeyboardButton(
                    text='Начать рассылку',
                    callback_data=f'send_all:{program_id}'
                )
