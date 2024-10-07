

but_sav = {
    12345: {  # приклад ID користувача
        "buttons": [
            "Кнопка 1",
            "Кнопка 2",
            "Кнопка 3",
            "Кнопка 4",
            "Кнопка 5",
            "Кнопка 6",
            "Кнопка 7",
            "Кнопка 8"
        ],
        "occupied": 0,
        "recent_buttons": []  # Список для збереження останніх використаних кнопок
    }
}

# Функція для використання кнопки і додавання її в список останніх використаних


def use_button(user_id, button_text):
    if user_id in but_sav and button_text in but_sav[user_id]["buttons"]:
        but_sav[user_id]["recent_buttons"].append(button_text)

        # Залишаємо лише останні три використані кнопки
        if len(but_sav[user_id]["recent_buttons"]) > 3:
            but_sav[user_id]["recent_buttons"].pop(
                0)  # Видаляємо найстарішу кнопку


# Використання кнопок
user_id = 12345
use_button(user_id, "Кнопка 3")
use_button(user_id, "Кнопка 5")
use_button(user_id, "Кнопка 2")
use_button(user_id, "Кнопка 4")

# Отримання трьох останніх використаних кнопок
recent_used_buttons = but_sav[user_id]["recent_buttons"]
print("Останні три використані кнопки:", recent_used_buttons)
