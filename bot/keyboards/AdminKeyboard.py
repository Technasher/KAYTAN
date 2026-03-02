from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать новую программу')],
    [KeyboardButton(text='Список активных программ')]
])