from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from data.state import but_sav


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ℹ'),
            KeyboardButton(text='🤪'),
            KeyboardButton(text='🌏'),
            KeyboardButton(text='🤪'),
            KeyboardButton(text='💬')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Оберіть дію',
    selective=True
)
