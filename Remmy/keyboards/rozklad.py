from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import Bot
import aiohttp
from datetime import datetime
import calendar
import requests
from bs4 import BeautifulSoup

from data.state import roz_stut, spus_gro, gru, kesh_day_roz_gr

short_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']

chas = ["0", "8:30-9:50", "10:05-11:25", "11:40-13:00", "13:15-14:35",
        "14:50-16:10", "16:25-17:45", "18:00-19:20", "19:30-20:50"]
para = ["0", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]


def create_rozk_keyboard(user_id: int) -> InlineKeyboardMarkup:
    # spus_gro[user_id] = []
    # g = spus_gro[user_id]
    keyboard_builder = InlineKeyboardBuilder()
    if user_id not in spus_gro:
        print("пустий список")
        keyboard_builder.add(InlineKeyboardButton(
            text="Додати групу", callback_data="ed_group"))

    else:

        grop = spus_gro[user_id]
        for g in grop:
            keyboard_builder.add(InlineKeyboardButton(
                text=str(g), callback_data=f"nulp_{str(g)}"))
        if len(grop) >= 5:
            pass
        else:
            keyboard_builder.add(InlineKeyboardButton(
                text="Додати групу", callback_data="ed_group"))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def create_rozk_lpnu(user_id: int, gr: str, st: int, tyj) -> InlineKeyboardMarkup:
    """st = calendar.weekday(datetime.now().year,
                          datetime.now().month, datetime.now().day)"""
    print(user_id)

    if st == 5 or st == 6:
        st = 0
    print("st ", st)
    if user_id not in kesh_day_roz_gr:
        kesh_day_roz_gr[user_id] = {}
    if user_id in kesh_day_roz_gr and f"{st}_{tyj}" in kesh_day_roz_gr[user_id]:
        if kesh_day_roz_gr[user_id][f"{st}_{tyj}"]:
            print("1")

            # roz = kesh_day_roz_gr[user_id][f"{st}_{tyj}"]
            roz_stut[user_id] = kesh_day_roz_gr[user_id][f"{st}_{tyj}"]

    else:
        print("2")

        url = f"https://student.lpnu.ua/students_schedule?studygroup_abbrname={
            gr}&semestr=1&semestrduration=1"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Отримуємо всі дні тижня
            day_headers = soup.find_all("span", class_="view-grouping-header")

            # schedule_list = []
            target_day = short_days[st]
            print("lkjsv", target_day)

            # Проходимо по кожному дню тижня
            for day_header in day_headers:
                day = day_header.get_text().strip()  # День тижня
                # print(f"\nДень тижня: {day}")
                if day == target_day:
                    # week = "Знаменник" if tyj == 0 else "Чисельник"
                    # day_schedule = f"\nТиждень на сайті: {week
                    #                                      }\n"
                    day_schedule = f"\nОбрана підгрупа: {day}\n"
                    # Шукаємо першу пару після дня
                    next_element = day_header.find_next_sibling()

                    # Проходимо по всіх парах до наступного дня або до кінця розкладу
                    kl = True
                    while next_element:
                        if next_element.name == 'h3':
                            pair_number = next_element.get_text()
                            # Шукаємо відповідний розклад для цієї пари
                            schedule_div = next_element.find_next(
                                'div', class_='stud_schedule')
                            if schedule_div:
                                rows = schedule_div.find_all(
                                    'div', class_='views-row')
                                for row in rows:

                                    week_color_div = row.find(
                                        'div', class_='week_color')
                                    if week_color_div:
                                        row_id = week_color_div.get('id')
                                    if tyj == 0:
                                        if week_color_div:

                                            # Додаємо лише пари для поточного тижня
                                            # week_type = "Чисельник" if row_id in [
                                            #    'group_chys', 'sub_1_chys', 'sub_2_chys', 'sub_3_chys', 'sub_4_chys'] else "Обидва тижні"

                                            # Виводимо інформацію про розклад
                                            content = row.get_text(
                                                separator='\n').strip()
                                            group_content = row.find(
                                                'div', class_='group_content')
                                            if group_content:
                                                # Видаляємо span з URL
                                                schedule_links = group_content.find_all(
                                                    'span', class_='schedule_url_link')
                                                dus = ""
                                                for span in schedule_links:
                                                    span.decompose()
                                                    dus = "💻"

                                            # Отримуємо текст без URL
                                                content_with_group = group_content.get_text(
                                                    separator='\n').strip()
                                                if not kl:
                                                    day_schedule += "\n➖➖➖➖➖➖➖➖➖➖"
                                                lin = content_with_group.splitlines()
                                                s_p = lin[1].strip()
                                                s_p_b_c, s_p_a_c = s_p.split(
                                                    ',', 1)
                                                s_p_m_c, s_p_aa_c = s_p_a_c.rsplit(
                                                    ',', 1)
                                                day_schedule += f"\n{para[int(pair_number)]}{dus} {
                                                    lin[0].strip()},{s_p_aa_c}\n🎓 {s_p_b_c}\n📍{s_p_m_c}\n🕗 {chas[int(pair_number)]}"
                                                # print(
                                                #    f"    {week_type}: {content}")
                                                kl = False
                                    else:
                                        if not week_color_div or row_id in ['group_full', 'sub_1_full', 'sub_2_full', 'sub_3_full', 'sub_4_full']:

                                            # week_type = "Знаменник" if row_id in [
                                            #    'group_znam', 'sub_1_znaml', 'sub_2_znam', 'sub_3_znaml', 'sub_4_znaml'] else "Обидва тижні"

                                            content = row.get_text(
                                                separator='\n').strip()
                                            group_content = row.find(
                                                'div', class_='group_content')
                                            if group_content:
                                                # Видаляємо span з URL
                                                schedule_links = group_content.find_all(
                                                    'span', class_='schedule_url_link')
                                                dus = ""
                                                for span in schedule_links:
                                                    span.decompose()
                                                    dus = "💻"

                                            # Отримуємо текст без URL
                                                content_with_group = group_content.get_text(
                                                    separator='\n').strip()
                                                if not kl:
                                                    day_schedule += "\n➖➖➖➖➖➖➖➖➖➖"
                                                lin = content_with_group.splitlines()
                                                s_p = lin[1].strip()
                                                s_p_b_c, s_p_a_c = s_p.split(
                                                    ',', 1)
                                                s_p_m_c, s_p_aa_c = s_p_a_c.rsplit(
                                                    ',', 1)
                                                day_schedule += f"\n{para[int(pair_number)]}{dus} {
                                                    lin[0].strip()},{s_p_aa_c}\n🎓 {s_p_b_c}\n📍{s_p_m_c}\n🕗 {chas[int(pair_number)]}"

                                                # print(
                                                #    f"    {week_type}: {content}")
                                                kl = False

                        next_element = next_element.find_next_sibling()

                        # Якщо наступний елемент є іншим днем тижня, виходимо з циклу
                        if next_element and next_element.name == 'span' and 'view-grouping-header' in next_element.get('class', []):
                            break
            roz_stut[user_id] = day_schedule.strip()
            kesh_day_roz_gr[user_id].update({
                f"{st}_{tyj}": day_schedule.strip()
            })


async def create_rozk_b_lpnu(user_id: int, gr: str, st) -> InlineKeyboardMarkup:
    gru[user_id] = gr

    if st == 5 or st == 6:
        st = 0
    keyboard_builder = InlineKeyboardBuilder()
    if st == 0:
        keyboard_builder.add(InlineKeyboardButton(
            text=f"🔼{short_days[st]}", callback_data="ignoreu"))
        for i in range(1, 5):
            keyboard_builder.add(InlineKeyboardButton(
                text=f"{short_days[i]}", callback_data=f"dayu_{i}"))
    else:
        for i in range(0, st):
            keyboard_builder.add(InlineKeyboardButton(
                text=f"{short_days[i]}", callback_data=f"dayu_{i}"))
        keyboard_builder.add(InlineKeyboardButton(
            text=f"🔼{short_days[st]}", callback_data="ignoreu"))
        for i in range(st+1, 5):
            keyboard_builder.add(InlineKeyboardButton(
                text=f"{short_days[i]}", callback_data=f"dayu_{i}"))
    keyboard_builder.add(InlineKeyboardButton(
        text=f"⚙Налаштування", callback_data="ignoreu"))

    keyboard_builder.adjust(5, 1)
    return keyboard_builder.as_markup()
