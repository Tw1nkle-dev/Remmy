from aiogram import Router, types, F, Bot
from keyboards import replyr, inliner
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


from keyboards import calen
from data.state import zmin_s, user_states, user_counters, ad, kli, user_data_ys, user_datas, but_sav, his

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if user_id not in but_sav:
        but_sav[user_id] = {
            "buttons": ["➕"] * 8,
            "occupied": 0
        }
    if user_id not in his:
        his[user_id] = {
            "buttons":
                ['📅Календар',
                 '✍Нотатки',
                 '📋Розклад',
                 '☰'],
                "occupied": 0,
                "recent_buttons": []
        }
    button_row1 = [
        KeyboardButton(text=his[user_id]["buttons"][i]) for i in range(len(his[user_id]["buttons"]))
    ]

    button_row2 = [
        KeyboardButton(text=but_sav[user_id]["buttons"][i]) for i in range(8)
    ]
    main = ReplyKeyboardMarkup(
        keyboard=[
            button_row1,
            button_row2
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Оберіть дію',
        selective=True
    )
    await message.answer("Вітаю, мене звати Ремчик і я створений, щоб тобі допомагати\n\nФункції, які у мене вже доступні:\n-різновидні розклади\n-календар\n-нотатник\n\nПереваги Remmy:\n-стабільність та швидкість\n-постійні оновлення та покращення", reply_markup=main)


@router.message(Command(commands=["calendar"]))
@router.message(F.text.lower() == "📅календар")
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_states[user_id] = "start"
    user_counters[user_id] = 0
    ad[user_id] = 0
    kli[user_id] = 0
    user_datas[user_id] = None
    user_data_ys[user_id] = None

    print(f"User ID: {user_id}, State: {user_states[user_id]}")

    zmin_s[user_id] = "calendar"

    keyboard = calen.create_calendar_keyboard(None, None, 0, 0, user_id)
    await message.answer("📅Календар", reply_markup=keyboard)


# @router.message(Command(commands=["roz"]))
@router.message(F.text.lower() == "📋розклад")
async def start_handler(message: Message):

    await message.answer("📋Розклад", reply_markup=inliner.rozk)


@router.message(F.text.lower() == "нулп")
async def start_handler(message: Message):
    await message.answer("Розклад НУЛП", reply_markup=inliner.rozk_lpnu)
