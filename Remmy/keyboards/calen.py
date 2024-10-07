from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from datetime import datetime
import calendar

from data.state import zmin_s, ad, user_states
# from callbacks.callr import


mon_ua = ["Січ.", "Лют.", "Берез.", "Квіт.", "Трав.", "Черв.",
          "Лип.", "Серп.", "Верес.", "Жовт.", "Листоп.", "Груд."]
mon_eng = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.",
           "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]

# дні тижня
dof_ua = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
dof_eng = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

stut = ["усі 👁", "заплановані⏰", "виконані✅", "скасовані❌"]


# def get_current_date():
#    return datetime.now().month, datetime.now().year, datetime.now().day

def get_current_date():
    return datetime.now().month, datetime.now().year, datetime.now().day


def create_calendar_keyboard(mon: int, year: int, userin: int, clik: int, user_id: int) -> InlineKeyboardMarkup:
    print("Userin*  ", userin)
    zmin = user_states[user_id]
    print("календар на початку  ", zmin)
    if zmin == ['start']:
        ad[user_id] = 0
    # print(zmin)
    current_day = 0
    zmin_s[user_id] = None
    if userin == 0:
        current_month, current_year, current_day = get_current_date()
    elif userin < 0:
        pass

    elif zmin == ['next_month']:
        current_year = year
        current_month = mon
        current_day = 0
    elif zmin == ['prev_month']:
        current_year = year
        current_month = mon
        if (current_month == datetime.now().month and current_year == datetime.now().year):
            current_month, current_year, current_day = get_current_date()
        print("curent   ", current_day, current_month, current_year)
    elif zmin == ['next_stut']:
        current_year = year
        current_month = mon
        if (current_month == datetime.now().month and current_year == datetime.now().year):
            current_month, current_year, current_day = get_current_date()
        print("curent next_stut   ", current_day, current_month, current_year)
    else:
        current_year = year
        current_month = mon
        current_day = 0

    print(current_day, current_month, current_year)
    # Визначаємо кількість днів у місяці
    if current_month in [1, 3, 5, 7, 8, 10, 12]:
        days_in_month = 31

    elif current_month == 2:
        if (current_year % 4 == 0 and current_year % 100 != 0) or current_year % 400 == 0:
            days_in_month = 29
        else:
            days_in_month = 28
    else:
        days_in_month = 30

    # Визначаємо день тижня для 1-го числа місяця
    day_n = calendar.weekday(current_year, current_month, 1)

    # Створюємо об'єкт клавіатури
    keyboard_builder = InlineKeyboardBuilder()
    if userin == 0:
        keyboard_builder.add(InlineKeyboardButton(
            text="<<", callback_data="ignore"))
    else:
        keyboard_builder.add(InlineKeyboardButton(
            text="<<", callback_data="prev_month"))

    keyboard_builder.add(InlineKeyboardButton(
        text=f"{mon_ua[current_month-1]} {current_year}", callback_data="ignore"))

    keyboard_builder.add(InlineKeyboardButton(
        text=">>", callback_data="next_month"))

    for i in range(0, 7):
        keyboard_builder.add(InlineKeyboardButton(
            text=f"{dof_ua[i]}", callback_data="ignore"))
    # Додаємо порожні кнопки для днів до 1-го числа місяця
    for _ in range(day_n):
        keyboard_builder.add(InlineKeyboardButton(
            text=" ", callback_data="ignore"))

    # Додаємо кнопки з номерами днів місяця
    if (current_day == datetime.now().day and current_month == datetime.now().month and current_year == datetime.now().year) or userin == 0:
        print("startapus")
        for day in range(1, current_day):
            keyboard_builder.add(InlineKeyboardButton(
                text=f"{day}", callback_data=f"day_{day}"))

        keyboard_builder.add(InlineKeyboardButton(
            text=f"{current_day} 🌞", callback_data="current_day"))

        for day in range(current_day+1, days_in_month+1):
            keyboard_builder.add(InlineKeyboardButton(
                text=f"{day}", callback_data=f"day_{day}"))

    else:
        for day in range(1, days_in_month+1):
            keyboard_builder.add(InlineKeyboardButton(
                text=f"{day}", callback_data=f"day_{day}"))

    buttons_in_last_row = (days_in_month + day_n) % 7

    # Перетворюємо клавіатуру у вигляд, де 7 кнопок в рядку (для кожного тижня)

    if buttons_in_last_row > 0:
        for _ in range(7 - buttons_in_last_row):
            keyboard_builder.add(InlineKeyboardButton(
                text=" ", callback_data="ignore"))
    print("ad  ", ad)
    if ad[user_id] == 1:

        keyboard_builder.add(InlineKeyboardButton(
            text="[➕]", callback_data="abolition"))
    elif ad[user_id] == 0:
        keyboard_builder.add(InlineKeyboardButton(
            text="➕", callback_data="add"))

    keyboard_builder.add(InlineKeyboardButton(
        # скасовані, виконані, заплановані, усі
        text=f"{stut[clik]}", callback_data=f"stut_{stut[clik]}"))

    keyboard_builder.add(InlineKeyboardButton(
        text=">", callback_data="next_stut"))

    keyboard_builder.adjust(3, 7, 7, 7, 7, 7, 7, 7, 7, 3)
    # Повертаємо клавіатуру як InlineKeyboardMarkup
    return keyboard_builder.as_markup()
