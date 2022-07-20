from aiogram import executor
from handlers import client
from bot_data import dp


async def on_startup(_):
    print("Bot Started")
    print("""_____________________________

    Автор бота - Encer
_____________________________""")


client.register_handlers_client(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
