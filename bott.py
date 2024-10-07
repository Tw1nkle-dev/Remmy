import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties


from aiogram.filters.callback_data import CallbackData


from config_read import config
# from keyboards import inliner
from handlers import u_commands
from callbacks import callr


async def main():
    bot = Bot(config.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    dp.include_routers(
        u_commands.router,
        callr.router

    )

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except:
        print("Бот примусово завершено.")
    finally:
        # Виконання дій перед завершенням роботи
        print("Закриття підключення до бота...")
        await bot.close()
        await dp.storage.close()

if __name__ == '__main__':

    asyncio.run(main())
