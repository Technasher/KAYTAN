from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать новую программу')],
    [KeyboardButton(text='Список активных программ')]
])

cancel_add_program_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data='cancel_add_program'
            )
        ]
    ]
)