from bot.keyboards.DeactivateProgramInline import get_deactivate_button
from bot.keyboards.SenderKeyboard import get_sender_button
from aiogram.types import InlineKeyboardMarkup


def get_program_manager_keyboard(program_id, message_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [get_sender_button(program_id)],
            [get_deactivate_button(program_id)]
        ]
    )
