import asyncio
import re
from aiogram import Router, types, Bot
from aiogram.types import Message, CallbackQuery
from datetime import datetime
import calendar


from keyboards import calen, inliner, rozklad
from data.state import zmin_s, kli, ad, user_states, user_counters, user_data_ys, user_datas, roz_stut, spus_gro, gru
router = Router()


last_callback_data = None
# clik = 0
callback_count1 = 0
# userin = 0


@router.callback_query(lambda callback_query: callback_query.data.startswith("day_") or callback_query.data.startswith("stut_") or callback_query.data in ["ignore", "current_day", "prev_month", "next_month", "add", "next_stut", "abolition"])
async def handle_callback(callback_query: types.CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id

    print(user_id)
    star = user_states[user_id]
    print("початок колбеків   ", star)

    print(f"Отримано callback_data: {callback_query.data}")
    if callback_query.data.startswith("day_"):
        # Отримуємо номер дня з callback_data

        selected_day = callback_query.data.split("_")[1]
        if ad[user_id] == 1:
            await bot.send_message(callback_query.from_user.id, f"Додати справу {selected_day}")
        else:
            await bot.send_message(callback_query.from_user.id, f"Обрано день: {selected_day}")
    elif callback_query.data == "ignore":
        await bot.send_message(callback_query.from_user.id, "Ігноровано")
    elif callback_query.data == "current_day":
        if ad[user_id] == 1:
            await bot.send_message(callback_query.from_user.id, "Запланувати на сьогодні")
        else:
            await bot.send_message(callback_query.from_user.id, "Що на сьогодні заплановано:")

    userin = user_counters[user_id]
    #    ad.clear()
    print("star  ", star)

    user_states[user_id] = callback_query.data

    if callback_query.data == "next_month":
        userin += 1
        if zmin_s[user_id] == 'calendar':
            userin = 1
        user_data = datetime.now().month+userin
        user_data_y = datetime.now().year
        n = user_data // 12
        m = user_data % 12
        if m == 0:
            m = 12
        print("user_data  ", user_data)
        print("n  ", n)
        if user_data > 12:
            user_data = m
            user_data_y += (1*n)
        print("user_data  ", user_data)

        print("userin+  ", userin)

        print("місяць1 ", user_data, user_data_y)
        # userin = callback_count

        user_datas[user_id] = user_data
        user_data_ys[user_id] = user_data_y
        # zber.append(userin)
        k = kli[user_id]

        keyboard = calen.create_calendar_keyboard(
            user_data, user_data_y, userin, k, user_id)
        user_counters[user_id] = userin
        # Оновлюємо повідомлення з новою клавіатурою
        await bot.edit_message_text(
            text="📅Календар",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard)

    elif callback_query.data == "prev_month":
        userin -= 1
        print("!userin-  ", userin)
        if userin == -1:
            userin += 1
        print("userin-  ", userin)

        user_data = datetime.now().month+userin
        user_data_y = datetime.now().year
        n = user_data // 12
        m = user_data % 12
        if m == 0:
            m = 12
        if user_data > 12:
            user_data = m
            user_data_y -= (1*n)
        elif user_data < datetime.now().month:
            user_data = datetime.now().month

        user_datas[user_id] = user_data
        user_data_ys[user_id] = user_data_y
        k = kli[user_id]

        keyboard = calen.create_calendar_keyboard(
            user_data, user_data_y, userin, k, user_id)
        user_counters[user_id] = userin
        await bot.edit_message_text(
            text="📅Календар",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard)
    if callback_query.data == "add":
        # await bot.send_message(callback_query.from_user.id, "вибір мов")
        if ad[user_id] == 0:
            ad[user_id] = 1

        keyboard = calen.create_calendar_keyboard(
            user_datas[user_id], user_data_ys[user_id], userin, kli[user_id], user_id)

        await bot.edit_message_text(
            text="📅Календар",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard)
    elif callback_query.data == "abolition":
        if ad[user_id] == 1:
            ad[user_id] = 0
        keyboard = calen.create_calendar_keyboard(
            user_datas[user_id], user_data_ys[user_id], userin, kli[user_id], user_id)
        await bot.edit_message_text(
            text="📅Календар",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard)
    elif callback_query.data == "next_stut":
        clik = kli[user_id]
        if clik >= 0 and clik <= 2:
            clik += 1
        else:
            clik = 0
        kli[user_id] = clik
        print("clik ", clik)

        keyboard = calen.create_calendar_keyboard(
            user_datas[user_id], user_data_ys[user_id], userin, kli[user_id], user_id)
        # Оновлюємо повідомлення з новою клавіатурою
        await bot.edit_message_text(
            text="📅Календар",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard)
    elif callback_query.data.startswith("stut_"):
        selec = callback_query.data.split("_")[1]

        await bot.send_message(callback_query.from_user.id, f"Обрано день: {selec}")


@router.callback_query(lambda callback_query: callback_query.data.startswith("dayu_") or callback_query.data in ["roz_univ", "nulp", "ed_group", "ignoreu"])
async def handle_callback(callback_query: types.CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id

    # roz_stut[user_id] = callback_query.data
    if callback_query.data == "roz_univ":

        await bot.send_message(callback_query.from_user.id, "Обери університет", reply_markup=inliner.univ)
    elif callback_query.data == "nulp":

        g = rozklad.create_rozk_keyboard(user_id)
        await bot.edit_message_text(
            text="Збережені групи:\n➖➖➖➖➖➖\nНе більше п'яти груп ",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=g)

    elif callback_query.data == "ed_group":
        # if roz_stut[user_id] == "ed_group":
        # Задаємо статус, що запит на додавання активний
        await bot.send_message(user_id, "Напиши назву групи, наприклад, КБ-208")

        # Очікування відповіді від користувача
        @router.message()
        async def check_group_format(message: types.Message):
            user_id = message.from_user.id
            st = calendar.weekday(datetime.now().year,
                                  datetime.now().month, datetime.now().day)
            # Перевірка формату введеної групи
            if re.match(r'^[А-ЯІЇЄҐ]{2}-\d{3}$', message.text) or re.match(r'^[А-ЯІЇЄҐ]{2}-\d{2}$', message.text):
                gr = message.text

                # Якщо у словнику ще немає запису для цього користувача, створюємо його
                if user_id not in spus_gro:
                    spus_gro[user_id] = []

                # Додаємо нову групу, якщо вона ще не була додана
                if len(spus_gro[user_id]) < 5:  # Перевірка на кількість груп
                    if gr not in spus_gro[user_id]:
                        spus_gro[user_id].append(gr)
                        await message.answer(f"Група {gr} збережена.")
                        await rozklad. create_rozk_lpnu(user_id, gr, st, 0)
                        g = await rozklad. create_rozk_b_lpnu(user_id, gr, st)
                        t = roz_stut[user_id]
                        g_message = ''.join(t)
                        await bot.send_message(user_id, text=g_message, reply_markup=g)
                    else:
                        await message.answer(f"Група {gr} вже була збережена.")
                else:
                    await message.answer("Не можна додати більше ніж 5 груп.")
            else:
                await message.answer("Неправильний формат групи. Напишіть у форматі: КБ-208.")
        # roz_stut[user_id] = ""
    elif callback_query.data == "ignoreu":
        await bot.send_message(callback_query.from_user.id, "Ігноровано")
    elif callback_query.data.startswith("dayu_"):
        selec = callback_query.data.split("_")[1]
        print("selec", selec)
        gr = gru[user_id]
        await rozklad. create_rozk_lpnu(user_id, gr, int(selec), 0)
        g = await rozklad. create_rozk_b_lpnu(user_id, gr, int(selec))
        t = roz_stut[user_id]
        g_message = ''.join(t)
        await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id, text=g_message, reply_markup=g)
