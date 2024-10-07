from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


rozk = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Створити власний",
                                 callback_data="roz_ad")
        ],
        [
            InlineKeyboardButton(text="Універи", callback_data="roz_univ")
        ],
        [
            InlineKeyboardButton(text="Збережені", callback_data="roz_saved")
        ]
    ]
)

univ = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="НУЛП",
                                 callback_data="nulp")

        ]
    ]
)
