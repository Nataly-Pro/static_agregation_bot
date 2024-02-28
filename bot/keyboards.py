from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Создаем объекты инлайн-кнопок
inline_buttons = [
    [InlineKeyboardButton(text='Час', callback_data='hour')],
    [InlineKeyboardButton(text='День', callback_data='day')],
    [InlineKeyboardButton(text='Месяц', callback_data='month')]
]

# Создаем объект инлайн-клавиатуры
inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_buttons, resize_keyboard=True)

